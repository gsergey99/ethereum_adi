const fs  = require('fs');
var Votaciones = artifacts.require("Votaciones");

module.exports = async function(deployer) {
   await deployer.deploy(Votaciones);
   storage = {'address': Votaciones.address};
	fs.writeFileSync('address.json',JSON.stringify(storage),'utf-8');
}
