#api = 'http://csm01:8080/client/api'
#admin
#apikey='f0Q70X5oTpax-b7bvyzDQf2t_rKaK0rWkLXhejPRqI4i6IgiSq5rJ5_KXo7pCE9-HpYqAYllg_Td9675H3E31Q'
#secret='8VxNvOkcKn7ibGAQhmI2L8frA7LmdN-IIGXNgmKJ_UxzWTpc487cFLE-vq0yLrXS6-dzL7luNecUyH0elrOA9g'
var cloudstack = new (require('cloudstack'))({
    apiUri: config.api_uri, // overrides process.env.CLOUDSTACK_API_URI
    apiKey: config.api_key, // overrides process.env.CLOUDSTACK_API_KEY
    apiSecret: config.api_secret // overrides process.env.CLOUDSTACK_API_SECRET
});

cloudstack.exec('listVirtualMachines', {}, function(error, result) {
    console.log(result);
});
