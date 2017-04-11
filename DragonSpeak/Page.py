from Lexical.Parser import Parser
from Enum.TriggerCategory import TriggerCategory

class Page:
    def __init__(self, engine, options = None):
        self.engine = engine
        self.options = options
        
        self.trigger_blocks = []
        self.trigger_handlers = dict()

        if self.options is not None:
            if self.options.on_discover_trigger is not None:
                self.on_discover_trigger = self.options.on_discover_trigger

    def set_trigger_handler(self, trigger, handler, description = None):
        trigger.description = description

        if (self.options.allow_handler_overrides):
            self.trigger_handlers[None, trigger] = handler
        else:
            if not self.trigger_handler_exists(trigger):
                self.trigger_handlers[None, trigger] = handler
            else: raise Exception('You cannot override the trigger handler for ({0}:{1}) without explicitly enabling trigger handler overrides in the page options.'
                                    .format(int(trigger.category), int(trigger.id)))

    def del_trigger_handler(self, trigger):
        for handler in dict(self.trigger_handlers):
            if handler[1] == trigger:
                del self.trigger_handlers[None, handler[1]]

    def insert(self, trigger_blocks):
        for block in trigger_blocks:
            initial_trigger = block[0]

            if initial_trigger.category is not TriggerCategory.Cause:
                raise Exception('You must only begin a paragraph with a cause trigger.',
                                'at index {0}, line {1}, column {2}.'.format(initial_trigger.index, initial_trigger.line, initial_trigger.column))

            if self.on_discover_trigger is not None:
                for trigger in block:
                    self.on_discover_trigger(trigger)

            self.trigger_blocks.append(block)

        return self

    def find_trigger_handler(self, trigger):
        return [handler[1] for handler in self.trigger_handlers.items() if handler[0][1] == trigger][0]

    def trigger_handler_exists(self, trigger):
        return len([handler for handler in self.trigger_handlers.items() if handler[0][1] == trigger]) > 0

    def execute_block(self, context, block):
        initial_trigger = block[0]

        if not self.trigger_handler_exists(initial_trigger):
            if self.options.ignore_unhandled_cause_triggers is False:
               raise Exception('There are no trigger handler(s) set for ({0}:{1}).'.format(int(initial_trigger.category), int(initial_trigger.id)),
                               'at index {0}, line {1}, column {2}.'.format(initial_trigger.index, initial_trigger.line, initial_trigger.column))
        else:
            if not self.find_trigger_handler(initial_trigger)(context, initial_trigger):
                return

        for i in range(1, len(block)):
            previous = block[i-1]
            current = block[i]

            current.cause = initial_trigger
            current.conditions = previous.conditions
            current.areas = previous.areas
            current.filters = previous.filters
            current.effects = previous.effects

            if not self.trigger_handler_exists(current):
               raise Exception('There are no trigger handler(s) set for ({0}:{1}).'.format(int(current.category), int(current.id)),
                               'at index {0}, line {1}, column {2}.'.format(current.index, current.line, current.column))
        
            
            if current.category is TriggerCategory.Cause:
                raise Exception('You cannot have sibling cause triggers within a paragraph.',
                                'at index {0}, line {1}, column {2}.'.format(current.index, current.line, current.column))

            elif current.category is TriggerCategory.Condition:
                if not self.find_trigger_handler(current)(context, current): return
                current.conditions.append(current)

            elif current.category is TriggerCategory.Area:
                if not self.find_trigger_handler(current)(context, current): return
                current.areas.append(current)

            elif current.category is TriggerCategory.Filter:
                if not self.find_trigger_handler(current)(context, current): return
                current.filters.append(current)
        
            elif current.category is TriggerCategory.Effect:
                if not self.find_trigger_handler(current)(context, current): return
                current.effects.append(current)

            else: raise Exception('The specified trigger category "{0}" does not exist.'.format(int(current.category)),
                                   'at index {0}, line {1}, column {2}.'.format(current.index, current.line, current.column))

    def execute(self, context, ids):
       for block in [(block) for id in ids for block in self.trigger_blocks if block[0].category is TriggerCategory.Cause and block[0].id == id]:
            self.execute_block(context, block)
