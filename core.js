// Run all probablity calculations
function generateProbability(isAllProbability) {
    // Reset old probability values
    for (let i = 0; i < mineGrid.length; i++) {
        for (let j = 0; j < mineGrid[i].length; j++) {
            mineGrid[i][j].mineArr = 0;
            mineGrid[i][j].probability = -1;
        }
    }
    hundredCount = 0;
    arrGrid = [];
    edgeArr = [];

    // Run basic logic rules
    edgeCount(mineGrid);
    let ret1 = true;
    let ret2 = true;
    while (ret1 == true || ret2 == true) {
        ret1 = ruleOne(mineGrid);
        ret2 = ruleTwo(mineGrid);
    }
    ruleThree(mineGrid);

    // Calculate arrangements and probabilities
    let index = findNextEdge(mineGrid, 0, 0);
    let i = index[0];
    let j = index[1];
    while (i > -1) {
        arrGrid.push({mine: null, r: i, c: j});
        if (j == numColumns - 1) {
            index = findNextEdge(mineGrid, i+1, 0);
            i = index[0];
            j = index[1];
        }
        else {
            index = findNextEdge(mineGrid, i, j+1);
            i = index[0];
            j = index[1];
        }
    }
    if (arrGrid.length > 0) {
        generateArrangements(mineGrid, arrGrid, 0);
        probabilityCalculation(edgeArr, mineGrid, isAllProbability);
    }
    else {
        let nonEdge = nonEdgeCount(mineGrid);
        let remainingMines = numMines - hundredCount;
        for (let i = 0; i < mineGrid.length; i++) {
            for (let j = 0; j < mineGrid[i].length; j++) {
                if (mineGrid[i][j].open == false && mineGrid[i][j].edge == false) {
                    mineGrid[i][j].probability = Math.round(remainingMines / nonEdge * 100);
                }
            }
        }

    }

}


// Label cells that border open cells and count how many "edges" are next to each cell
function edgeCount(mineGrid) {
    for (let i = 0; i < mineGrid.length; i++) {
        for (let j = 0; j < mineGrid[i].length; j++) {
            let count = 0;
            if (mineGrid[i][j].open == true) {
                mineGrid[i][j].edge = false;
                // Left
                if (j > 0) {
                    if (mineGrid[i][j-1].open == false) {
                        mineGrid[i][j-1].edge = true;
                        count++;
                    }
                }
                // Upper Left
                if (i > 0 && j > 0) {
                    if (mineGrid[i-1][j-1].open == false) {
                        mineGrid[i-1][j-1].edge = true;
                        count++;
                    }
                }
                // Up
                if (i > 0) {
                    if (mineGrid[i-1][j].open == false) {
                        mineGrid[i-1][j].edge = true;
                        count++;
                    }
                }
                // Upper Right
                if (i > 0 && j < (numColumns-1)) {
                    if(mineGrid[i-1][j+1].open == false) {
                        mineGrid[i-1][j+1].edge = true;
                        count++;
                    }
                }
                // Right
                if (j < (numColumns-1)) {
                    if (mineGrid[i][j+1].open == false) {
                        mineGrid[i][j+1].edge = true;
                        count++;
                    }
                }
                // Bottom Right
                if (i < (numRows-1) && j < (numColumns-1)) {
                    if (mineGrid[i+1][j+1].open == false) {
                        mineGrid[i+1][j+1].edge = true;
                        count++;
                    }
                }
                // Bottom
                if (i < (numRows-1)) {
                    if (mineGrid[i+1][j].open == false) {
                        mineGrid[i+1][j].edge = true;
                        count++;
                    }
                }
                // Bottom Left
                if (i < (numRows-1) && j > 0) {
                    if (mineGrid[i+1][j-1].open == false) {
                        mineGrid[i+1][j-1].edge = true;
                        count++;
                    }
                }
            }
            mineGrid[i][j].edgeCount = count;
        }
    }
}

// Label isolated cells that have independently determined probabilities
function ruleThree(mineGrid) {
    for (let i = 0; i < mineGrid.length; i++) {
        for (let j = 0; j < mineGrid[i].length; j++) {
            if (mineGrid[i][j].edgeCount > 2) {
                let count = 0;
                // Left
                if (j > 0) {
                    if (mineGrid[i][j-1].edge == true && openCount(mineGrid, i, j-1) == 1) {
                        count++;
                    }
                }
                // Upper Left
                if (i > 0 && j > 0) {
                    if (mineGrid[i-1][j-1].edge == true && openCount(mineGrid, i-1, j-1) == 1) {
                        count++;
                    }
                }
                // Up
                if (i > 0) {
                    if (mineGrid[i-1][j].edge == true && openCount(mineGrid, i-1, j) == 1) {
                        count++;
                    }
                }
                // Upper Right
                if (i > 0 && j < (numColumns-1)) {
                    if(mineGrid[i-1][j+1].edge == true && openCount(mineGrid, i-1, j+1) == 1) {
                        count++;
                    }
                }
                // Right
                if (j < (numColumns-1)) {
                    if (mineGrid[i][j+1].edge == true && openCount(mineGrid, i, j+1) == 1) {
                        count++;
                    }
                }
                // Bottom Right
                if (i < (numRows-1) && j < (numColumns-1)) {
                    if (mineGrid[i+1][j+1].edge == true && openCount(mineGrid, i+1, j+1) == 1) {
                        count++;
                    }
                }
                // Bottom
                if (i < (numRows-1)) {
                    if (mineGrid[i+1][j].edge == true && openCount(mineGrid, i+1, j) == 1) {
                        count++;
                    }
                }
                // Bottom Left
                if (i < (numRows-1) && j > 0) {
                    if (mineGrid[i+1][j-1].edge == true && openCount(mineGrid, i+1, j-1) == 1) {
                        count++;
                    }
                }
                if (count == mineGrid[i][j].edgeCount) {
                    let probability = Math.round(mineGrid[i][j].neighbors / mineGrid[i][j].edgeCount * 100);
                    // Left
                    if (j > 0) {
                        mineGrid[i][j-1].probability = probability;
                    }
                    // Upper Left
                    if (i > 0 && j > 0) {
                        mineGrid[i-1][j-1].probability = probability;
                    }
                    // Up
                    if (i > 0) {
                        mineGrid[i-1][j].probability = probability;
                    }
                    // Upper Right
                    if (i > 0 && j < (numColumns-1)) {
                        mineGrid[i-1][j+1].probability = probability;
                    }
                    // Right
                    if (j < (numColumns-1)) {
                        mineGrid[i][j+1].probability = probability;
                    }
                    // Bottom Right
                    if (i < (numRows-1) && j < (numColumns-1)) {
                        mineGrid[i+1][j+1].probability = probability;
                    }
                    // Bottom
                    if (i < (numRows-1)) {
                        mineGrid[i+1][j].probability = probability;
                    }
                    // Bottom Left
                    if (i < (numRows-1) && j > 0) {
                        mineGrid[i+1][j-1].probability = probability;
                    }
                }
            }
        }
    }
}

// Find the next "edge" cell with an assigned logical probability starting from the given index
function findNextEdge(mineGrid, x, y) {
    for (let i = x; i < numRows; i++) {
        for (let j = y; j < numColumns; j++) {
            if (mineGrid[i][j].edge == true && mineGrid[i][j].probability < 0) {
                return [i,j];
            }
        }
        y = 0;
    }
    return [-1, -1];
}

// Recursively generate all possible mine arrangements for open edges
function generateArrangements(mineGrid, grid, index) {
    let i = grid[index].r;
    let j = grid[index].c;
    if (canBeMine(mineGrid, grid, i, j) == true) {
        let patternYes = JSON.parse(JSON.stringify(grid));
        patternYes[index].mine = true;
        if (index < grid.length - 1) {
            generateArrangements(mineGrid, patternYes, index+1);
        }
        else {
            edgeArr.push(patternYes);
        }
    }
    if (canNotBeMine(mineGrid, grid, i, j) == true) {
        let patternNo = JSON.parse(JSON.stringify(grid));
        patternNo[index].mine = false;
        if (index < grid.length - 1) {
            generateArrangements(mineGrid, patternNo, index+1);
        }
        else {
            edgeArr.push(patternNo);
        }
    }
}

// Calculate probabilities from given mine arrangements
function probabilityCalculation(edgeArr, mineGrid, allProbability) {
    // Store where mines are placed in each arrangement and find the total number of arrangements
    let arrCount = 0;
    let nonEdge = nonEdgeCount(mineGrid);
    for (let k = 0; k < edgeArr.length; k++) {
        let minesPlaced = 0;
        for (let i = 0; i < edgeArr[k].length; i++) {
            if (edgeArr[k][i].mine == true) {
                minesPlaced++;
            }
        }
        let remainingMines = numMines - minesPlaced - hundredCount;
        if (remainingMines >= 0 && remainingMines <= nonEdge) {
            let nonEdgeCombinations = combinations(nonEdge, remainingMines);
            for (let i = 0; i < edgeArr[k].length; i++) {
                if (edgeArr[k][i].mine == true) {
                    mineGrid[edgeArr[k][i].r][edgeArr[k][i].c].mineArr += nonEdgeCombinations;
                }
            }
            arrCount += nonEdgeCombinations;
            for (let i = 0; i < mineGrid.length; i++) {
                for (let j = 0; j < mineGrid[i].length; j++) {
                    if (mineGrid[i][j].open == false && mineGrid[i][j].edge == false) {
                        mineGrid[i][j].mineArr += remainingMines / nonEdge * nonEdgeCombinations
                    }
                }
            }
        }
    }

    // Calculate probability of each cell by dividing the number of arrangements with mines in each cell by total arrangements
    for (i = 0; i < mineGrid.length; i++) {
        for (j = 0; j < mineGrid[i].length; j++) {
            if (mineGrid[i][j].edge == true && mineGrid[i][j].probability < 0) {
                let edgeProbability = Math.round(mineGrid[i][j].mineArr / arrCount * 100);
                if (allProbability == false && (edgeProbability == 100 || edgeProbability == 0)) {
                    mineGrid[i][j].probability = edgeProbability;
                }
                if (allProbability == true) {
                    mineGrid[i][j].probability = edgeProbability;
                }
            }
            if (mineGrid[i][j].open == false && mineGrid[i][j].edge == false && mineGrid[i][j].probability < 0) {
                let nonEdgeProbability = Math.round(mineGrid[i][j].mineArr / arrCount * 100);
                if (allProbability == false && (nonEdgeProbability == 100 || nonEdgeProbability == 0)) {
                    mineGrid[i][j].probability = nonEdgeProbability;
                }
                if (allProbability == true) {
                    mineGrid[i][j].probability = nonEdgeProbability;
                }
            }
        }
    }
    // console.log("arrCount:");
    // console.log(arrCount);
    // console.log("nonEdge:");
    // console.log(nonEdge);
}

// Count how many cells are neither open nor bordering open cells
function nonEdgeCount(mineGrid) {
    let count = 0;
    for (i = 0; i < mineGrid.length; i++) {
        for (j = 0; j < mineGrid[i].length; j++) {
            if (mineGrid[i][j].open == false && mineGrid[i][j].edge == false) {
                count++;
            }
        }
    }
    return count;
}

// Create a sample mine grid
const numRows = 5;
const numColumns = 5;
const numMines = 5;

const mineGrid = [];
for (let i = 0; i < numRows; i++) {
    mineGrid[i] = [];
    for (let j = 0; j < numColumns; j++) {
        mineGrid[i][j] = {
            open: false,
            edge: false,
            edgeCount: 0,
            neighbors: 0,
            mineArr: 0,
            probability: -1
        };
    }
}

// Set random mines
let minesPlaced = 0;
while (minesPlaced < numMines) {
    const randomRow = Math.floor(Math.random() * numRows);
    const randomColumn = Math.floor(Math.random() * numColumns);
    if (!mineGrid[randomRow][randomColumn].open) {
        mineGrid[randomRow][randomColumn].open = true;
        minesPlaced++;
    }
}

// Run probability calculations
generateProbability(false);

// Print probabilities
for (let i = 0; i < mineGrid.length; i++) {
    for (let j = 0; j < mineGrid[i].length; j++) {
        console.log(`Cell (${i}, ${j}): Probability = ${mineGrid[i][j].probability}%`);
    }
}

// Label cells that must be a mine by basic logic rules
function ruleOne(mineGrid) {
    let ret = false;
    for (let i = 0; i < mineGrid.length; i++) {
        for (let j = 0; j < mineGrid[i].length; j++) {
            if (mineGrid[i][j].edgeCount > 0 && mineGrid[i][j].neighbors == mineGrid[i][j].edgeCount - probabilityZeroCount(mineGrid, i, j)) {
                // Left
                if (j > 0) {
                    if (mineGrid[i][j-1].edge == true && mineGrid[i][j-1].probability < 0) {
                        mineGrid[i][j-1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Upper Left
                if (i > 0 && j > 0) {
                    if (mineGrid[i-1][j-1].edge == true && mineGrid[i-1][j-1].probability < 0) {
                        mineGrid[i-1][j-1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Up
                if (i > 0) {
                    if (mineGrid[i-1][j].edge == true && mineGrid[i-1][j].probability < 0) {
                        mineGrid[i-1][j].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Upper Right
                if (i > 0 && j < (numColumns-1)) {
                    if(mineGrid[i-1][j+1].edge == true && mineGrid[i-1][j+1].probability < 0) {
                        mineGrid[i-1][j+1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Right
                if (j < (numColumns-1)) {
                    if (mineGrid[i][j+1].edge == true && mineGrid[i][j+1].probability < 0) {
                        mineGrid[i][j+1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Bottom Right
                if (i < (numRows-1) && j < (numColumns-1)) {
                    if (mineGrid[i+1][j+1].edge == true && mineGrid[i+1][j+1].probability < 0) {
                        mineGrid[i+1][j+1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Bottom
                if (i < (numRows-1)) {
                    if (mineGrid[i+1][j].edge == true && mineGrid[i+1][j].probability < 0) {
                        mineGrid[i+1][j].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
                // Bottom Left
                if (i < (numRows-1) && j > 0) {
                    if (mineGrid[i+1][j-1].edge == true && mineGrid[i+1][j-1].probability < 0) {
                        mineGrid[i+1][j-1].probability = 100;
                        hundredCount++;
                        ret = true;
                    }
                }
            }
        }
    }
    return ret;
}


// Count how many cells with zero probability are around a cell
function probabilityZeroCount(mineGrid, i, j) {
    let count = 0;
    // Left
    if (j > 0) {
        if (mineGrid[i][j-1].probability == 0) {
            count++;
        }
    }
    // Upper Left
    if (i > 0 && j > 0) {
        if (mineGrid[i-1][j-1].probability == 0) {
            count++;
        }
    }
    // Up
    if (i > 0) {
        if (mineGrid[i-1][j].probability == 0) {
            count++;
        }
    }
    // Upper Right
    if (i > 0 && j < (numColumns-1)) {
        if (mineGrid[i-1][j+1].probability == 0) {
            count++;
        }
    }
    // Right
    if (j < (numColumns-1)) {
        if (mineGrid[i][j+1].probability == 0) {
            count++;
        }
    }
    // Bottom Right
    if (i < (numRows-1) && j < (numColumns-1)) {
        if (mineGrid[i+1][j+1].probability == 0) {
            count++;
        }
    }
    // Bottom
    if (i < (numRows-1)) {
        if (mineGrid[i+1][j].probability == 0) {
            count++;
        }
    }
    // Bottom Left
    if (i < (numRows-1) && j > 0) {
        if (mineGrid[i+1][j-1].probability == 0) {
            count++;
        }
    }
    return count;
}


// Label cells that must not be a mine by basic logic rules
function ruleTwo(mineGrid) {
    let ret = false;
    for (let i = 0; i < mineGrid.length; i++) {
        for (let j = 0; j < mineGrid[i].length; j++) {
            if (mineGrid[i][j].edgeCount > 0 && mineGrid[i][j].neighbors == probabilityHundredCount(mineGrid, i, j)) {
                // Left
                if (j > 0) {
                    if (mineGrid[i][j-1].edge == true && mineGrid[i][j-1].probability < 0) {
                        mineGrid[i][j-1].probability = 0;
                        ret = true;
                    }
                }
                // Upper Left
                if (i > 0 && j > 0) {
                    if (mineGrid[i-1][j-1].edge == true && mineGrid[i-1][j-1].probability < 0) {
                        mineGrid[i-1][j-1].probability = 0;
                        ret = true;
                    }
                }
                // Up
                if (i > 0) {
                    if (mineGrid[i-1][j].edge == true && mineGrid[i-1][j].probability < 0) {
                        mineGrid[i-1][j].probability = 0;
                        ret = true;
                    }
                }
                // Upper Right
                if (i > 0 && j < (numColumns-1)) {
                    if(mineGrid[i-1][j+1].edge == true && mineGrid[i-1][j+1].probability < 0) {
                        mineGrid[i-1][j+1].probability = 0;
                        ret = true;
                    }
                }
                // Right
                if (j < (numColumns-1)) {
                    if (mineGrid[i][j+1].edge == true && mineGrid[i][j+1].probability < 0) {
                        mineGrid[i][j+1].probability = 0;
                        ret = true;
                    }
                }
                // Bottom Right
                if (i < (numRows-1) && j < (numColumns-1)) {
                    if (mineGrid[i+1][j+1].edge == true && mineGrid[i+1][j+1].probability < 0) {
                        mineGrid[i+1][j+1].probability = 0;
                        ret = true;
                    }
                }
                // Bottom
                if (i < (numRows-1)) {
                    if (mineGrid[i+1][j].edge == true && mineGrid[i+1][j].probability < 0) {
                        mineGrid[i+1][j].probability = 0;
                        ret = true;
                    }
                }
                // Bottom Left
                if (i < (numRows-1) && j > 0) {
                    if (mineGrid[i+1][j-1].edge == true && mineGrid[i+1][j-1].probability < 0) {
                        mineGrid[i+1][j-1].probability = 0;
                        ret = true;
                    }
                }
            }
        }
    }
    return ret;
}

// Count how many cells with one hundred probability are around a cell
function probabilityHundredCount(mineGrid, i, j) {
    let count = 0;
    // Left
    if (j > 0) {
        if (mineGrid[i][j-1].probability == 100) {
            count++;
        }
    }
    // Upper Left
    if (i > 0 && j > 0) {
        if (mineGrid[i-1][j-1].probability == 100) {
            count++;
        }
    }
    // Up
    if (i > 0) {
        if (mineGrid[i-1][j].probability == 100) {
            count++;
        }
    }
    // Upper Right
    if (i > 0 && j < (numColumns-1)) {
        if (mineGrid[i-1][j+1].probability == 100) {
            count++;
        }
    }
    // Right
    if (j < (numColumns-1)) {
        if (mineGrid[i][j+1].probability == 100) {
            count++;
        }
    }
    // Bottom Right
    if (i < (numRows-1) && j < (numColumns-1)) {
        if (mineGrid[i+1][j+1].probability == 100) {
            count++;
        }
    }
    // Bottom
    if (i < (numRows-1)) {
        if (mineGrid[i+1][j].probability == 100) {
            count++;
        }
    }
    // Bottom Left
    if (i < (numRows-1) && j > 0) {
        if (mineGrid[i+1][j-1].probability == 100) {
            count++;
        }
    }
    return count;
}

// Count how many cells that are open are around a cell
function openCount(mineGrid, i, j) {
    let count = 0;
    // Left
    if (j > 0) {
        if (mineGrid[i][j-1].open == true) {
            count++;
        }
    }
    // Upper Left
    if (i > 0 && j > 0) {
        if (mineGrid[i-1][j-1].open == true) {
            count++;
        }
    }
    // Up
    if (i > 0) {
        if (mineGrid[i-1][j].open == true) {
            count++;
        }
    }
    // Upper Right
    if (i > 0 && j < (numColumns-1)) {
        if (mineGrid[i-1][j+1].open == true) {
            count++;
        }
    }
    // Right
    if (j < (numColumns-1)) {
        if (mineGrid[i][j+1].open == true) {
            count++;
        }
    }
    // Bottom Right
    if (i < (numRows-1) && j < (numColumns-1)) {
        if (mineGrid[i+1][j+1].open == true) {
            count++;
        }
    }
    // Bottom
    if (i < (numRows-1)) {
        if (mineGrid[i+1][j].open == true) {
            count++;
        }
    }
    // Bottom Left
    if (i < (numRows-1) && j > 0) {
        if (mineGrid[i+1][j-1].open == true) {
            count++;
        }
    }
    return count;
}
