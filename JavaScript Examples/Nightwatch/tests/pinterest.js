
module.exports = {

    before : function(_browser) {
      console.log('This function is called before all tests run')
    },

    beforeEach : function(_browser) {
      console.log('This function is called before each test case is run')
    },

    afterEach : function(_browser, done){
      setTimeout(function(){done();}, 200);
      console.log('This function is called after each test case is run')
    },
   
    after : function(_browser, done){
      setTimeout(function(){done();},200);
      console.log('This function is called after all tests have run')
    },

    'Test a path through all the error messages on the sign up form': function(_browser) {
    _browser
      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 )
      // attempt to sign up with blank email address and blank password
      .keys(['\uE004']) //presses TAB key
      .keys(['\uE004']) //presses TAB key
      .keys(['\uE006']) //presses ENTER key.
      .waitForElementVisible('.errorTooltip.emailError', 5000)
      .verify.visible('.errorTooltip.emailError') 
      .assert.containsText('.errorTooltip.emailError', 'You missed a bit! Don\'t forget to add your email.')

      // attempt to sign up setting email to a 4 character string and blank password
      .setValue('#userEmail', 'test' )
      .keys(['\uE004']) //presses TAB key
      .keys(['\uE006']) //presses ENTER key.
      .waitForElementVisible('.errorTooltip.emailError', 5000)
      .verify.visible('.errorTooltip.emailError') 
      .assert.containsText('.errorTooltip.emailError', 'Hmm...that doesn\'t look like an email address.')
      
      // attempt to sign up with a valid email address and blank password
      .clearValue('#userEmail')
      .setValue('#userEmail', 'justaseleniumtest@gmail.com')
      .keys(['\uE006']) //presses ENTER key.
      .waitForElementVisible('.errorTooltip.emailError.passwordError', 5000)
      .verify.visible('.errorTooltip.emailError.passwordError') 
      .assert.containsText('.errorTooltip.emailError.passwordError', 'Your password is too short. You need 6+ characters.')
      
      // attempt to sign up with a valid email address and a weak password
      .setValue('#userPassword', '123456')
      .click('.signupButton')
      .waitForElementVisible('.errorTooltip.emailError.passwordError', 5000)
      .verify.visible('.errorTooltip.emailError.passwordError') 
      .assert.containsText('.errorTooltip.emailError.passwordError', 'Please make a stronger password.')

      // attempt to sign up with an email address which is already taken
      .setValue('#userPassword', '1234567!')
      .click('.signupButton')
      .waitForElementVisible('.errorTooltip.emailError.passwordError', 5000)
      .verify.visible('.errorTooltip.emailError.passwordError') 
      .pause(4000)
      .assert.containsText('.errorTooltip.emailError.passwordError', 'Deja vu! That email is taken. Forgotten your password?')
      .verify.visible('a[href="/password/reset/"]')
    },

    'Try to login with valid credentials': function( _browser ) {
    _browser
      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 )
      .setValue('#userEmail', 'justaseleniumtest@gmail.com')
      .setValue('#userPassword', 'thisisatest')
      .keys(['\uE006']) //presses ENTER key.
      .waitForElementVisible('.Input.Module.field', 10000) // waits for the searchbar to be visible before continuing
},


}
