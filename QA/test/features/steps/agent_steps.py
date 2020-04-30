from behave import given, when, then, step
import main

@given('we have behave installed')
def step_impl(context):
    pass

@when('we implement tests')
def step_impl(context):
    # assert number > 1 or number == 0
    main()


@then('behave will test them for us!')
def step_impl(context):
    context.tests_count