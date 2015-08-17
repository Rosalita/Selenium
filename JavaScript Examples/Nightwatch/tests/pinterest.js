
module.exports = {

    'Try to login with no username or password': function( _browser ) {
    _browser
      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 )
      .click('.emailLogin')
      .waitForElementVisible('.Button.Module.btn[type=submit]', 5000)
      .click('.Button.Module.btn[type=submit]')
      .pause(2000)
      .verify.visible('input[class=hasError]')
      .end();
    },

// To Do
//  'Try to login with wrong username and password': function( _browser ) {
//  },
// 'Try to log in with valid credentials': function( _browser ) {
//  },

}
