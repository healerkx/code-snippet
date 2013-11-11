import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Maze Reader
 * @author zmyu
 *
 */
public class MazeReader {

	public int[][] getMaze(String fileName) {
		File file = new File(fileName);
		int[][] maze = null;
		
		try {
			LineNumberReader lnr = new LineNumberReader(new FileReader(file));
			
			int count = 0;
			String line = lnr.readLine();
			int len = 0;
			List<String> lines = new ArrayList<String>();
			while (line != null) {
				count++;
				len = line.length();
				lines.add(line);
				line = lnr.readLine();
			}
			maze = new int[count][len];
			for (int i = 0; i < count; ++i) {
				line = lines.get(i);
				for (int j = 0; j < len; ++j) {
					maze[i][j] = line.charAt(j) - '0'; 
				}
			}
			
			lnr.close();
			return maze;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return null;
		
	}
	
	public static void main(String[] args) {
		
		int[][] maze = new MazeReader().getMaze("d:\\maze1.txt");
		for (int i = 0; i < maze.length; ++i) {
			for (int j = 0; j < maze[i].length; ++j) {
				System.out.print(maze[i][j]);
			}
			System.out.println();
		}
		System.out.println();
	}
}
