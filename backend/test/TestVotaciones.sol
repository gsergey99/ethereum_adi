pragma solidity >= 0.5.0 < 0.8.0;
pragma experimental ABIEncoderV2;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Votaciones.sol";

contract TestVotaciones {

    function testCrearVotacion() public {
        /*Crear una votación correctamente con la red reiniciada*/
        Votaciones votacion = Votaciones(DeployedAddresses.Votaciones());
        uint expected_id = 0;

        Assert.equal(votacion.crearVotacion(), expected_id, "Expected votation id");
    }

    function testAddCandidate() public {
        /*Añadir un candidato correctamente*/
        Votaciones votacion = Votaciones(DeployedAddresses.Votaciones());
        uint id_votacion = votacion.crearVotacion();
        string memory nombre_candidato = "Jose";
        votacion.addCandidato(id_votacion, nombre_candidato);

        Assert.equal(votacion.listaCandidatos(id_votacion).length, 1, "Expected length list candidates");

        string[] memory index_candidato = votacion.listaCandidatos(id_votacion);

        Assert.equal(index_candidato[0], "Jose", "Expected candidate name");
    }

    function testGanador() public {
        /*Obtener el candidato ganador en una votación*/
        Votaciones votacion = Votaciones(DeployedAddresses.Votaciones());
        uint id_votacion = votacion.crearVotacion();
        string memory nombre_candidato = "Jose";

        votacion.addCandidato(id_votacion, nombre_candidato);
        votacion.cerrarLista(id_votacion);
        votacion.votar(id_votacion, nombre_candidato);
        votacion.cerrarEncuesta(id_votacion);

        Assert.equal(votacion.ganador(id_votacion), "Jose", "Expected winner");
    }

    function testResults() public {
        /*Obtener resultado de los votos de cada candidato*/
        Votaciones votacion = Votaciones(DeployedAddresses.Votaciones());
        uint id_votacion = votacion.crearVotacion();
        string memory nombre_candidato = "Jose";

        votacion.addCandidato(id_votacion, nombre_candidato);
        votacion.cerrarLista(id_votacion);
        votacion.votar(id_votacion, nombre_candidato);
        votacion.cerrarEncuesta(id_votacion);

        Assert.equal(votacion.listaVotos(id_votacion).length, 1, "Expected result length");

        uint64[] memory lista_votos = votacion.listaVotos(id_votacion);
        uint64 numero_votos = lista_votos[0];

        Assert.equal(numero_votos, uint(1), "Expected value");
    }
}
