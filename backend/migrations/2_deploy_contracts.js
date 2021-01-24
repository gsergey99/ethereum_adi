const Votaciones = artifacts.require("Votaciones");

module.exports = function(deployer) {
  deployer.deploy(Votaciones);
};
