pragma solidity >=0.5.0 <0.8.0;
pragma experimental ABIEncoderV2;

contract Votaciones {

    enum Estado { Creada, Abierta, Cerrada }

    struct Candidato {
        string nombre;
        uint64 votos;
        bool exists;
    }

    struct Votacion {
        address propietario;
        Estado estado;
        string ganador;
    }

    mapping(uint => Votacion) private votaciones;
    uint private contadorVotaciones = 0;

    mapping(uint => mapping(string => Candidato)) private candidatos;
    mapping(uint => string[]) private candidatos_nombres;
    
    mapping(uint => mapping(address => bool)) private votantes;

    //Sección de funciones del propietario
    function crearVotacion() external returns (uint) {
        Votacion memory nueva_votacion;
        uint id = contadorVotaciones;

        nueva_votacion.propietario = msg.sender;
        nueva_votacion.estado = Estado.Creada;
        votaciones[id] = nueva_votacion;

        //Necesario? Eliminar en caso contario
        string[] memory lista_candidatos;
        candidatos_nombres[id] = lista_candidatos;

        contadorVotaciones++;

        /* Otra posibilidad
        nueva_votacion = Votacion({
            propietario: msg.sender,
            estado: Estado.Creada,
            ganador: Candidato("", 0)
        }); */

        return id;
    }

    
    function addCandidato(uint id_votacion, string calldata nombre_candidato) external {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
        Votacion memory votacion = votaciones[id_votacion];

        require(msg.sender == votacion.propietario, "No eres el propietario de esta votacion."); 
        require(votacion.estado == Estado.Creada, "La lista de candidatos ya esta cerrada.");
        require(!candidatos[id_votacion][nombre_candidato].exists, "El candidato ya existe.");
        
        Candidato memory nuevo_candidato;
        nuevo_candidato.nombre = nombre_candidato;
        nuevo_candidato.votos = 0;
        nuevo_candidato.exists = true;
        candidatos[id_votacion][nombre_candidato] = nuevo_candidato;

        string[] storage candidatos_votacion = candidatos_nombres[id_votacion];
        candidatos_votacion.push(nombre_candidato);
    }

    function cerrarLista(uint id_votacion) external {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
        Votacion storage votacion = votaciones[id_votacion];

        require(msg.sender == votacion.propietario, "No eres el propietario de esta votacion."); 
        require(votacion.estado == Estado.Creada, "La lista de candidatos ya esta cerrada.");
        require(candidatos_nombres[id_votacion].length > 0, "Se necesita al menos un candidato para poder cerrar la lista.");

        votacion.estado = Estado.Abierta;
    }

    function cerrarEncuesta(uint id_votacion) external {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
        Votacion storage votacion = votaciones[id_votacion];

        require(msg.sender == votacion.propietario, "No eres el propietario de esta votacion."); 
        require(votacion.estado != Estado.Creada, "La lista de candidatos aun no esta cerrada.");
        require(votacion.estado != Estado.Cerrada, "La votacion ya ha sido cerrada.");

        string[] memory lista_candidatos = candidatos_nombres[id_votacion];
        string memory curr_ganador = lista_candidatos[0];
        string memory curr_candidato;
	    uint64 max_votos = 0;
        uint64 curr_votos;
        for (uint16 i = 0; i < lista_candidatos.length; i++) {
            curr_candidato = lista_candidatos[i];
	        curr_votos = candidatos[id_votacion][curr_candidato].votos;
            if (curr_votos > max_votos) {
                max_votos = curr_votos;
                curr_ganador = curr_candidato;   
	        }
        }

        votacion.ganador = curr_ganador;
	    votacion.estado = Estado.Cerrada;

    }
    
    // ----- Seccion de otros usuarios -----

    function listaCandidatos(uint id_votacion) external view returns (string[] memory) {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");

        string[] memory list_candidatos = candidatos_nombres[id_votacion];
        return list_candidatos;
    }

    function votar(uint id_votacion, string calldata nombre_candidato) external {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
        require(votaciones[id_votacion].estado != Estado.Creada, "La lista de candidatos aun no esta cerrada.");
        require(votaciones[id_votacion].estado != Estado.Cerrada, "La votacion ya ha sido cerrada.");
        require(!votantes[id_votacion][msg.sender], "Ya has votado en esta encuesta.");

        Candidato storage candidato = candidatos[id_votacion][nombre_candidato];
        require(candidato.exists, "El candidato no existe");
        candidato.votos++;

        votantes[id_votacion][msg.sender] = true;
    }

    function ganador(uint id_votacion) external view returns (string memory) {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
        Votacion memory votacion = votaciones[id_votacion];

        require(votacion.estado == Estado.Cerrada, "La votacion aun no ha finalizado.");

        return votacion.ganador;
    }

    function listaVotos(uint id_votacion) external view returns (uint64[] memory) {
        
        require(id_votacion < contadorVotaciones, "La votacion no existe.");
	
	Votacion memory votacion = votaciones[id_votacion];
	require(votacion.estado == Estado.Cerrada, "La votación no ha terminado");
	
        string[] memory lista_candidatos = candidatos_nombres[id_votacion];
        uint n_candidatos = lista_candidatos.length;

        uint64[] memory lista_votos = new uint64[](n_candidatos);
        string memory curr_candidato;
        
        for (uint16 i = 0; i < n_candidatos; i++) {
            curr_candidato = lista_candidatos[i];
            lista_votos[i] = candidatos[id_votacion][curr_candidato].votos;
        }

        return lista_votos;
    }

}
