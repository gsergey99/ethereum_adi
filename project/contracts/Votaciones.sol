//pragma solidity ^0.5.16;
//pragma solidity >=0.5.0 <0.7.5;
pragma experimental ABIEncoderV2;
pragma solidity >=0.5.0 <0.6.0;

contract Votaciones {

    enum Estado {Creada, Abierta, Cerrada }
 
    
    int[] balance;

function push(int _number) public{
   balance.push(_number);     
} 

function get () public view returns (int [] memory){
	return balance;
}

}

