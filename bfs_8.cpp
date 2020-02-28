#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

const int PUZZLE_LENGTH = 9;

const int EMPTY = 0;

struct Puzzle
{
    int state[PUZZLE_LENGTH];
    int gapLocation;
};

struct breadthPuzzle
{
    Puzzle puzzle;
    int parent;
};

const Puzzle SOLVED_PUZZLE = { { 1,2,3,4,5,6,7,8,EMPTY } };

// Check if the provided puzzle is actually solvable or not
// Credit for formula to: http://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
bool isSolvable(const Puzzle& puz)
{
    int inversions = 0;

    for ( int i = 0; i < PUZZLE_LENGTH; i++ )
        for ( int j = i + 1; j < PUZZLE_LENGTH; j++ )
            if ( puz.state[j] > puz.state[i] && puz.state[i] != EMPTY && puz.state[j] != EMPTY )
                inversions++;

    // If the amount of inversions is even the puzzle can be solved
    return inversions % 2 == 0;

}

// Checks if the 2 provided puzzles are the same
bool puzzleTheSame(const Puzzle& puz1, const Puzzle& puz2)
{
    for ( int length = 0; length < PUZZLE_LENGTH; length++ )
        if ( puz1.state[length] != puz2.state[length] ) return false;
    return true;
}

bool puzzleExists(const Puzzle& currentPuzzle, vector<breadthPuzzle>& currentRoute)
{
    for ( int i = 0; i < currentRoute.size(); i++ )
        if ( puzzleTheSame(currentRoute[i].puzzle, currentPuzzle) )
            return true;
    return false;
}

// Checks if the provided puzzle is solved
bool isSolved(const Puzzle& solution)
{
    return puzzleTheSame(SOLVED_PUZZLE, solution);
}

bool canNorth(int gapLocation)
{
    return gapLocation > 2;
}

bool canEast(int gapLocation)
{
    return (gapLocation != 2 && gapLocation != 5 && gapLocation != 8);
}

bool canSouth(int gapLocation)
{
    return gapLocation < 6;
}

bool canWest(int gapLocation)
{
    return (gapLocation != 0 && gapLocation != 3 && gapLocation != 6);
}

int north(int gap)
{
    return gap - 3;
}

int east(int gap)
{
    return gap + 1;
}

int south(int gap)
{
    return gap + 3;
}

int west(int gap)
{
    return gap - 1;
}

Puzzle createNextPuzzle(Puzzle currentPuzzle, int pos)
{
    int temp = currentPuzzle.state[pos];
    currentPuzzle.state[currentPuzzle.gapLocation] = temp;
    currentPuzzle.state[pos] = EMPTY;
    currentPuzzle.gapLocation = pos;
    return currentPuzzle;
}

void solvePuzzle(vector<breadthPuzzle>& currentRoute, int i, int futurePos)
{
    Puzzle currentPuzzle = createNextPuzzle(currentRoute[i].puzzle, futurePos);

    if ( !puzzleExists(currentPuzzle, currentRoute) )
    {
        breadthPuzzle candidate{ currentPuzzle, i };
        currentRoute.push_back(candidate);
    }
}

void breadthFirst(Puzzle initalPuzzle)
{
    // Origin has no parent, thus -1 as start.
    vector<breadthPuzzle> breadthVector = { { initalPuzzle, -1 } };
    int i = 0;

    while ( i < breadthVector.size() && !isSolved(breadthVector[i].puzzle) )
    {
        Puzzle currentPuzzle = breadthVector[i].puzzle;
        int gapLocation = currentPuzzle.gapLocation;

        if ( canNorth(gapLocation) ) solvePuzzle(breadthVector, i, north(gapLocation));
        if ( canEast(gapLocation) ) solvePuzzle(breadthVector, i, east(gapLocation));
        if ( canSouth(gapLocation) ) solvePuzzle(breadthVector, i, south(gapLocation));
        if ( canWest(gapLocation) ) solvePuzzle(breadthVector, i, west(gapLocation));
        i++;
    }
}

int main()
{
    Puzzle toSolve = { {1,2,3,4,6,5,8,7,EMPTY}, 8 };
    //Breadth-First: Duration in seconds = 72;
    //Depth-First: Duration in seconds = 15;

    high_resolution_clock::time_point t1 = high_resolution_clock::now();

    if ( isSolvable(toSolve) )
    {
        cout << "Puzzle Solvable\n";
        breadthFirst(toSolve);
    }
    else
        cout << "Puzzle insolvable, stopping\n";

    high_resolution_clock::time_point t2 = high_resolution_clock::now();
    auto durationSec = duration_cast<seconds>(t2 - t1).count();

    cout << "Duration in seconds of function: " << durationSec << endl;
}
