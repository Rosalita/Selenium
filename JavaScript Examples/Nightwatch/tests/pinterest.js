
module.exports = {

    //To stop this test running set disabled to true
    disabled :false,

    before : function(_browser) {
      // This function is called before all tests run
      console.log('Setting up tests')
    },

    beforeEach : function(_browser) {
      // This function is called before each test case runs
      console.log('Setting up test case')
    },

    afterEach : function(_browser, done){
      // This function is called after each test case is run
      console.log('Test case finished')
      // Timeout must be set to prevent errors
      setTimeout(function(){done();}, 200);
    },

    after : function(_browser, done){
      // This function is called after all tests have run
      console.log('All tests finished')
       _browser.end();
      // Timeout must be set to prevent errors
      setTimeout(function(){done();},200);
    },
    'Test a path through all the error messages on the sign up form': function(_browser) {
    _browser

      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 ) // wait 1 second for the body of the page to load
      .assert.title("Pinterest: discover and save creative ideas") // test the title of the page is correct

      //test that the email and password input boxes are both present on the page
      .assert.elementPresent('#userEmail')
      .assert.elementPresent('#userPassword')

      // asserts attributeEquals and attributeContains can be used to test the placeholder text these input boxes
      .assert.attributeEquals('#userEmail','placeholder','Email') // assert 'Email' equals 'Email'
      .assert.attributeContains('#userPassword','placeholder','password') // assert 'Create a password' contains 'password'

      // attempt to sign up with blank email address and blank password
      // navigation through forms can be done by sending key presses using .keys
      .keys(['\uE004']) //presses TAB key
      .keys(['\uE004']) //presses TAB key
      .keys(['\uE006']) //presses ENTER key
      .waitForElementVisible('.errorTooltip.emailError', 5000)
      .verify.visible('.errorTooltip.emailError') // if a verify fails, the test will continue
      .assert.visible('.errorTooltip.emailError') // if an assert fails, the test will stop
      .assert.containsText('.errorTooltip.emailError', 'You missed a bit! Don\'t forget to add your email.') // Test the message

      // attempt to sign up setting email to a 4 character string and leaving password blank
      .setValue('#userEmail', 'test' ) // type 'test' into the email input box
      .click('.signupButton') // An alternative to pressing tab and enter is to just click on the sign up button
      .waitForElementVisible('.errorTooltip.emailError', 5000)
      .verify.visible('.errorTooltip.emailError')
      .assert.containsText('.errorTooltip.emailError', 'Hmm...that doesn\'t look like an email address.')

      // attempt to sign up with a valid email address and blank password
      .clearValue('#userEmail') // delete the existing text 'test' from the email input box
      .setValue('#userEmail', 'justaseleniumtest@gmail.com')
      .click('.signupButton')
      // assert that the email error message is now a password error message
      // the email error element is <div id="firstStepTooltip" class="errorTooltip emailError" style="display: block;">
      // the password error element is <div id="firstStepTooltip" class="errorTooltip emailError passwordError" style="display: block;">
      // so need to check the element with ID firstStepTooltip has the class errorTooltip emailError passwordError
      // this can be done with the assert cssClassPresent however there is a bug in Nightwatch version v0.7.10
      // The below line can be uncommented when this issue is fixed https://github.com/nightwatchjs/nightwatch/issues/608
      // .assert.cssClassPresent('#firstStepTooltip', 'errorTooltip emailError passwordError')
      // however cssClassNotPresent is currently working, so for now will assert that the error element is not an email error
      .assert.cssClassNotPresent('#firstStepTooltip', 'errorTooltip emailError')
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
      // as well as implicit waits such as waitForElementVisible, Nightwatch can also handle explicit waits
      .pause(5000) // this is an explicit wait for 5 seconds
      .assert.containsText('.errorTooltip.emailError.passwordError', 'Deja vu! That email is taken. Forgotten your password?')
      //the css selector below asserts <a href="/password/reset> is visible, this is the forgotten password link
      .assert.visible('a[href="/password/reset/"]')

      // refresh the page and test that error messages are no longer present
      .refresh()
      .assert.elementNotPresent('.errorTooltip.emailError')
      .assert.elementNotPresent('.errorTooltip.emailError.passwordError')

    },

    'Login with valid credentials and do some testing': function( _browser ) {
    _browser
      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 )
      .setValue('#userEmail', 'justaseleniumtest@gmail.com') //type in email
      .setValue('#userPassword', 'thisisatest') // type in password
      .keys(['\uE006']) //press ENTER key.
      .waitForElementVisible('.Input.Module.field', 10000) // wait upto 10 seconds for the searchbar to be visible
      .click('.Button.DropdownButton.Module.btn.categoriesHeader')  // click on the categories dropdown
      .pause(5000)
      // assert that all the categories are present on the categories menu
      .assert.containsText('.categoriesWrapper ', 'Home feed\nPopular\nEverything\nAnimals & Pets\nArchitecture\nArt\nCars & Motorcycles')
      .assert.containsText('.categoriesWrapper ', '\nCelebrations & Events\nCelebrities\nDesign\nEducation\nFilm, Music & Books\nFood & Drink')
      .assert.containsText('.categoriesWrapper ', '\nGardening\nGeek\nHair & Beauty\nHealth & Fitness\nHistory\nHobbies & Crafts\nHome Décor')
      .assert.containsText('.categoriesWrapper ', '\nHumour\nIllustrations & Posters\nKids & Parenting\nMen\'s Fashion\nOutdoors\nPhotography')
      .assert.containsText('.categoriesWrapper ', '\nProducts\nQuotes\nScience & Nature\nSports\nTattoos\nTechnology\nTravel\nWeddings\nWomen\'s Fashion')
      // For debugging purposes it is possible to output all the text from the categories menu by uncommenting the function below
      //.getText('.categoriesWrapper ', function(result){
      //  console.log(result.value)
      //});
      .click('a[data-category="popular"') // click on the Popular option
      .pause(5000)
       // urls can be tested using urlContains or urlEquals
      .assert.urlContains('popular')
      .assert.urlEquals('https://www.pinterest.com/categories/popular/')
      .back() // click the back button on the browser
      .waitForElementVisible('button[data-element-type="215"]', 5000) // wait for invite friends button to be visible
      .click('button[data-element-type="215"]') // click on invite friends button
      .waitForElementVisible('.mailIcon', 5000) // wait for the mail icon to display

      // send an invite to a unique email address which has not been sent an invite before
      // this email address needs to be unique each time the test runs
      // to meet both of these criteria, the test is goign to enter a valid gmail alias
      // gmail supports email aliases by adding '+something' to the first part of the address
      // an email sent to an alias is received by the main gmail account
      // to make a valid email for the test, append the current epochtime to current users address
      // the alias would look something like: justaseleniumtest+1437131756@gmail.com

      var epochTimeNow = new Date().valueOf()
      var emailAlias = 'justaseleniumtest' + String(epochTimeNow) + '@gmail.com'
      _browser
      .setValue('.emailInput', emailAlias) // type in the email alias
      .keys(['\uE006']) // and press ENTER
      .waitForElementVisible('.inviteConfirm', 5000)
      .assert.containsText('.inviteConfirm', 'Invitations sent!')

      // test sending a second invite to the same email address again
      .setValue('.emailInput', emailAlias)
      .keys(['\uE006'])
      .waitForElementVisible('form[class="standardForm"]', 10000)
      .assert.containsText('.body', 'Oops! You\'ve already invited that person.')
},

}
