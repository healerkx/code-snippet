
/**
 * Position
 * @author zmyu
 *
 */
public class Position {
	private int row = -1;
	private int col = -1;
	
	public Position(int row, int col) {
		this.row = row;
		this.col = col;
	}
	
	public int row() {
		return row;
	}
	
	public int col() {
		return col;
	}
}
