
/**
 * 0 means on the way
 * @author Administrator
 *
 */
public class Maze {
	
	// Maze as member
	private int[][] maze = null;
	
	//
	private int row1 = -1;
	private int col1 = -1;
	private int row2 = -1;
	private int col2 = -1;
	
	private Path path = new Path();
	// /*0*/ 1 2 3 4
	private static int[] directs = new int[] { 0, 1, 1, 0, 0, -1, -1, 0 };

	public Maze(int[][] maze) {
		this.maze = maze;
	}
	
	public Maze(int[][] maze, int row1, int col1, int row2, int col2) {
		this.maze = maze;
		this.row1 = row1;
		this.col1 = col1;
		this.row2 = row2;
		this.col2 = col2;
	}
	
	public Maze() {
		
	}
	
	/**
	 *   4
	 * 3 0 1
	 *   2
	 * @param x1 from
	 * @param y1 from
	 * @param x2 to
	 * @param y2 to
	 * @return
	 */
	private static int optimizedDirect(int x1, int y1, int x2, int y2) {
		int result = -1;
		if (x1 > x2) {
			result = 3;
		} else if (x1 < x2) {
			result = 1;
		} else {
			if (y1 > y2) {
				result = 4;
			} else if (y1 < y2) {
				result = 2;
			} else {
				return result = 0;
			}
		}
		return result;
	}
	
	public static int nextRow(int row, int direct) {
		return row + directs[(direct - 1) * 2];
	}
	
	public static int nextCol(int col, int direct) {
		return col + directs[(direct - 1) * 2 + 1];
	}
	
	private Step tryStep(int curRow, int curCol, int times, int came) {
		int od = optimizedDirect(curRow, curCol, row2, col2);
		
		int curTimes = times;
		int direct = 0;
		while (curTimes < 4) {
			direct = od + curTimes;
			direct = direct % 4;
			direct = (direct == 0)? 4 : direct;
			
			if (against(direct, came)) {
				curTimes++;
				continue;
			}
			
			int nextRow = nextRow(curRow, direct);
			int nextCol = nextCol(curCol, direct);
			if (onWay(nextRow, nextCol)) {
				return new Step(curRow, curCol, curTimes + 1, direct);
			}
			curTimes++;
		}
		
		return null;
	}


	private boolean against(int d1, int d2) {
		return (Math.abs(d1 - d2) == 2);
	}

	private boolean onWay(int row, int col) {
		return (maze[row][col] == 0);
	}
	
	public Path getPath() {
		return path;
	}
	
	public void findWay() {
		
		int curRow = row1;
		int curCol = col1;
		Step step = tryStep(curRow, curCol, 0, 0);
		if (step == null) {
			return;		// No way
		}
		path.add(step);	// first step
		
		int times = 0;
		Position pos = null;
		while (true) {
			
			if (step != null) {
				pos = step.nextPosition();
				if (pos.col() == col2 && pos.row() == row2) {
					System.out.println("OK");
					break;
				}
				Step lastStep = path.latest();
				step = tryStep(pos.row(), pos.col(), times, lastStep.direct());
			} else {
				Step lastStep = path.latest();
				Step prevStep = path.previous();
				step = tryStep(lastStep.row(), lastStep.col(), lastStep.times(), prevStep.direct());
				if (step != null)
					path.update(step);
				else {
					path.back();
				}
				continue;
			}

			if (step == null) {
				
			} else {
				path.add(step);
				System.out.println(String.format("[%1$d,%2$d]", step.row(), step.col()));
			}
		}

		
	}
	
	public static void main(String[] args) {
		int[][] mazeArray = new MazeReader().getMaze("maze1.txt");
		Maze maze = new Maze(mazeArray, 5, 4, 7, 18);
		maze.findWay();
		System.out.println();
		System.out.println();
		Path path = maze.getPath();
		for (Step step : path.getSteps()) {
			System.out.println(String.format("[%1$d, %2$d]", step.row(), step.col()));
		}
		
	}
}
