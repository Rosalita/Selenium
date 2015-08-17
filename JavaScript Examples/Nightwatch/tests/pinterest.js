
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

    'Try to login with no username or password': function( _browser ) {
    _browser
      .url('https://www.pinterest.com/')
      .waitForElementVisible( 'body', 1000 )
      .click('.emailLogin')
      .waitForElementVisible('.Button.Module.btn[type=submit]', 5000)
      .click('.Button.Module.btn[type=submit]')
      .pause(2000)
      .verify.visible('input[class=hasError]')
      
    },

// To Do
//  'Try to login with wrong username and password': function( _browser ) {
//  },
// 'Try to log in with valid credentials': function( _browser ) {
//  },

}
