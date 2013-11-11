import java.util.ArrayList;
import java.util.List;

/**
 * Path
 * @author zmyu
 *
 */
public class Path {

	private List<Step> steps = new ArrayList<Step>();
	
	public Path() {
		
	}
	
	public void add(Step step) {
		steps.add(step);
	}
	
	public List<Step> getSteps() {
		return steps;
	}
	
	public Step latest() {
		return steps.get(steps.size() - 1);
	}

	public Step previous() {
		return steps.get(steps.size() - 2);
	}

	public void update(Step step) {
		steps.set(steps.size() - 1, step);
		
	}

	public void back() {
		steps.remove(steps.size() - 1);
	}
	
}
