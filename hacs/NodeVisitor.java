package hacs;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author Sairachana paladugu
 * @version 2.0 :: Update Code to 2021 Design Standards
 */

abstract public class NodeVisitor {

	public NodeVisitor() {
	}

	public NodeVisitor(Object visitee) {
	}

	abstract public void visitFacade(Facade facade);

	abstract public void visitCourse(Course course);

	abstract public void visitAssignment(Assignment assignment);

}