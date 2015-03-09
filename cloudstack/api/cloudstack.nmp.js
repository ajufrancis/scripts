var cloudstack = require('cloudstack')
  , templateId = 1
  , serviceOfferingId = 1
  , zoneId = 1;

client.deployVirtualMachine(templateId, serviceOfferingId, zoneId, function(result) {
    var virtualMachineId = result.vmid;

    result.emitter.on('success', function() {
        console.log('Machine deployed successfully and it is ready to use!');
    });

    result.emitter.on('fail', function() {
        console.log('Machine failed to deploy.');
    });
});
