const area = 400;
let playerTurn = true;
//The board variable refers to the 16 squares in this 4x4 tic tac toe game
let board = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
//The winCombos variable refers to which spots on the board the player or Ai has to control to win the game
let winCombos = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [0, 5, 10, 15], [3, 6, 9, 12]
  ]
let winner = false;

let canvas = document.getElementById("board");
let ctx = canvas.getContext("2d");
ctx.moveTo(area*.25,0);
ctx.lineTo(area*.25,area);
ctx.moveTo(area*.50,0);
ctx.lineTo(area*.50,area);
ctx.moveTo(area*.75,0);
ctx.lineTo(area*.75,area);
ctx.moveTo(0, area*.25);
ctx.lineTo(area,area*.25);
ctx.moveTo(0, area*.50);
ctx.lineTo(area,area*.50);
ctx.moveTo(0, area*.75);
ctx.lineTo(area,area*.75);
ctx.strokeStyle = "#ffffff";
ctx.lineWidth=10;
ctx.stroke();


window.onload = function() {
  init();
}

//Runs on reset button click
function reset() {
  winner = false;
  let index;
  document.getElementsByClassName("winScreen")[0].innerHTML = "";
  for (let i = 0; i < 16; i++) {
    index = document.getElementById(i);
    index.innerHTML = "";
    index.style.backgroundColor = "";
  }
  board = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
  winCombos = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [0, 5, 10, 15], [3, 6, 9, 12]]
}

//Runs on window load to generate the board
function init() {
  winner = false;
  let count = 0;
  for (let j = 0; j < 4; j++) {
    for (let i = 0; i < 4; i++) {
      let element = document.createElement("div");
      element.className = "cells";
      element.id = count;
      count++;
      element.addEventListener('click', function() { play(element) }, false);
      let node = document.createElement("ul");
      document.getElementsByClassName("gameContainer")[0].appendChild(element);
    }
    let lineBreak = document.createElement("br");
    document.getElementsByClassName("gameContainer")[0].appendChild(lineBreak);
  }
}

//This function places Xs or Os on the board, depending on whose turn it is
function play(element) {
  if (playerTurn && board[element.id] < 99 && !winner) {
    playerTurn = false;
    let node = document.createElement("ul");
    node.innerHTML = "X"
    document.getElementById(element.id).appendChild(node);
    board[element.id] = "player";
    changeWinCombos(element.id);
    check(element);
  } 
  else if (!playerTurn && !element.id) {
    let node = document.createElement("ul");
    node.innerHTML = "O"
    document.getElementById(element).appendChild(node);
    board[element] = "ai";
    playerTurn = true;
    changeWinCombos(element);
    check(element);
  }
}

//This function involves changing the winCombo variable list to reflect who moved where as the game progresses
function changeWinCombos(id) {
  winCombos.forEach(function(outerId, indexOne) {
    outerId.forEach(function(innerId, indexTwo) {
      if (innerId == id) {
        if (playerTurn) {
          winCombos[indexOne][indexTwo] = "ai";
        }
        else {
          winCombos[indexOne][indexTwo] = "player";
        }
      }
    });
  });
}

//This is the main function of the game. It runs after every single move.
//The same logic here can be slightly adjusted to fit larger games such as 5x5 or 6x6.
//First, it reviews the altered winCombos list
//If there's a 4 in a row combo, a winner is declared
//If there's a 3 in a row combo, the Ai moves to win or block the player from winning
//Besides that, it generates a list of "clean" winCombos that have no player pieces in them
//The computer will move on whichever one of those clean combos it holds the most pieces in. Randomly selected if the number of choices is higher than one. This is so the game gives you something a little new each time
//If there's no more clean combos, it will move randomly to play out the rest of the tie game. Blocking if needed.
function check(move) {
  let indexOfCleanWinCombos = [];
  //The 'count' variables are a 0 through 4 value that refer to how many times a player has played in a single winCombo
  let playerCount = 0;
  let aiCount = 0;
  let block = -1;
  winCombos.forEach(function(arr, indexOne) {
    playerCount = 0;
    aiCount = 0;
    arr.forEach(function(innerValues, indexTwo) {
      if (innerValues === "player") {
        playerCount ++;
      }
      if (innerValues === "ai") {
        aiCount ++;
      }
    });
    if (aiCount == 3) {
      for (let j = 0; j < arr.length; j++) {
        if (!isNaN(arr[j])) {
          play(arr[j]);
        }
      }
    }
    if (playerCount == 3) {
      for (let j = 0; j < arr.length; j++) {
        if (!isNaN(arr[j])) {
          block = arr[j];
        }
      }
    }
    if (playerCount == 4 || aiCount == 4) {
      declareWinner(playerCount, aiCount, indexOne);
    }
    if (playerCount == 0) {
      indexOfCleanWinCombos.push([aiCount, arr]);
    }
  });
  if (block != -1) {
    play(block);
  }
  if (!winner) {
    if (indexOfCleanWinCombos.length == 0) {
      playRandom();
      return
    }
    let randomNumber = 0;
    let indexes = findHighest(indexOfCleanWinCombos);
    if (indexes.length > 1) {
      randomNumber = Math.floor(Math.random()*indexes.length);
    }
    aiFindSpot();
    
    function aiFindSpot() {
      let secondRandom = Math.floor(Math.random()*4);
      if (indexOfCleanWinCombos[indexes[randomNumber]][1][secondRandom] == "ai") {
        aiFindSpot();
      }
      else {
        play(indexOfCleanWinCombos[indexes[randomNumber]][1][secondRandom]);
      }
    }
  }
}

//This function takes the array of numbers and finds the index position(s) of the highest number(s). 
function findHighest(indexArray) {
  let highest = indexArray[0][0];
  let indexes = [];
  for (let i = 0; i < indexArray.length; i++) {
    if (indexArray[i][0] > highest) {
    //Found new highest, reset everything
      indexes = [i];
      highest = indexArray[i][0];
    }
    else if (indexArray[i][0] == highest) {
      indexes.push(i);
    }
  }
  return indexes
}

function playRandom() {
  let arr = [];
  board.forEach(function(value) {
    if (!isNaN(value)) {
      arr.push(value);
    }
  });
  let random = Math.floor(Math.random()*arr.length);
  if (isNaN(arr[random])) {
    document.getElementsByClassName("winScreen")[0].innerHTML = "Tie game..."
  } 
  else {
    play(arr[random]);
  }
}

function declareWinner(playerCount, aiCount, index) {
  winCombos = [
    [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], 
    [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], 
    [0, 5, 10, 15], [3, 6, 9, 12]
  ]
  for (let i = 0; i < winCombos[index].length; i++) {
    document.getElementsByClassName("cells")[winCombos[index][i]].style.backgroundColor = "yellow";
  }
  winner = true;
  if (playerCount == 4) {
    document.getElementsByClassName("winScreen")[0].innerHTML = "You won!";
  }
  else if (aiCount == 4) {
    document.getElementsByClassName("winScreen")[0].innerHTML = "You lose!";
  }
}
