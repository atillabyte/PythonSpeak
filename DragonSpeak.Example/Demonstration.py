from DragonSpeak import *

script = '''
 (0:31) When someone says {hello world},
   (1:70) and the string {loremipsum} has 10 characters,
     (5:103) give 2.5 cookies to any user present.'''

def on_discover_trigger(trigger):
    print('discovered trigger: ({0}:{1})'.format(int(trigger.category), int(trigger.id)))
    return

def on_cause(context, trigger):
    message = trigger.get_string(0)

    print('{0} said {1}'.format(context, message))
    return True

def on_condition(context, trigger):
    string = trigger.get_string(0)
    length = trigger.get_number(1)

    return len(string) >= length

def on_effect(context, trigger):
    cookies = trigger.get_number(0)

    print('{0} received {1} cookie(s)!'.format(context, cookies))
    return True

engine = DragonSpeakEngine()
page = engine.load_script(script, DragonSpeakPageOptions(
                    ignore_unhandled_cause_triggers = True,
                    on_discover_trigger = on_discover_trigger
                ))

page.set_trigger_handler(Trigger(TriggerCategory.Cause, 31), on_cause)
page.set_trigger_handler(Trigger(TriggerCategory.Condition, 70), on_condition)
page.set_trigger_handler(Trigger(TriggerCategory.Effect, 103), on_effect)

page.execute('bob', [31])