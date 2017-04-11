# PythonSpeak

DragonSpeak –_or DS for short_– is a functional scripting language used in Furcadia.

## Example

```python
engine = DragonSpeakEngine()
page = engine.load_script(script)

def on_cause(context, trigger):
    return True
    
def on_condition(context, trigger):
    return True
    
def on_effect(context, trigger):
    return True

page.set_trigger_handler(Trigger(TriggerCategory.Cause, 1), on_cause)
page.set_trigger_handler(Trigger(TriggerCategory.Condition, 1), on_condition)
page.set_trigger_handler(Trigger(TriggerCategory.Effect, 1), on_effect)

page.execute('bob', [1])
```

Disclaimer: _This website is in no way affiliated with, authorized, maintained, sponsored or endorsed by the Dragon's Eye Productions or any of its affiliates or subsidiaries._
