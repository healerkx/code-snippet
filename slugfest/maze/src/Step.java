import java.util.HashMap;

/**
 * 
 * @author zmyu
 *
 */
public class Step {

	private int row = -1;
	
	private int col = -1;
	
	private int times = 0;
	
	private int direct = 0;
	
	private static HashMap<Integer, Step> cache = new HashMap<Integer, Step>();
	
	public Step(int row, int col, int times, int direct) {
		this.row = row;
		this.col = col;
		this.times = times;
		this.direct = direct;
	}
	
	public Step(int row, int col) {
		this.row = row;
		this.col = col;
	}
	
	public int row() {
		return row;
	}
	
	public int col() {
		return col;
	}
	
	public int times() {
		return times;
	}
	
	public int direct() {
		return direct;
	}
	
	public void times(int times) {
		this.times = times;
	}
	
	public void direct(int direct) {
		this.direct = direct;
	}
	
	public Position nextPosition() {
		return new Position(Maze.nextRow(row, direct), Maze.nextCol(col, direct));
	}
	
	public boolean equals(Object other) {
		if (other.getClass().equals(this.getClass())) {
			Step otherStep = (Step) other;
			if (otherStep.row() == row && otherStep.col() == col
					&& otherStep.times() == times && otherStep.direct() == direct) {
				return true;
			}
		}
		return false;
	}
	
	public static int hashCode(int a, int b) {
		int code = 0;
		code = a << 16;
		code |= b;
		return code;
	}
	
	public static Step getStep(int row, int col) {
		int code = hashCode(row, col);
		Step step = cache.get(code);
		if (step == null) {
			step = new Step(row, col);
			cache.put(code, step);
		}
		return step;
	}

	public int hashCode() {
		return hashCode(row, col);
	}
	
}
