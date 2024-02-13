package hacs;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.text.DateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 *
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 *
 */
public class AssignmentTest {

    Assignment assignment;

    @BeforeEach
    void start() {
        assignment = new Assignment();
    }

    /**
     * tests setDueDate Method of Assignment class
     */
    @Test
    void testSetDueDate() {
        Date today = new Date();
        assignment.setDueDate(today);
        assertEquals(today, assignment.dueDate);
    }


    /**
     * tests setAssignmentSpec Method of Assignment Class
     */
    @Test
    void testSetAssignmentSpecification() {
        assignment.setAssignmentSpecification("SETASSIGNMENTSPECIFICATION");
        assertEquals("SETASSIGNMENTSPECIFICATION", assignment.assignmentSpecification);
    }

    /**
     * tests isOverDue Method of Assignment Class
     */
    @Test
    void testIsOverDue() {
        Date dueDate = new GregorianCalendar(2022, Calendar.MARCH, 22).getTime();
        assignment.setDueDate(dueDate);
        assertTrue(assignment.isOverDue());
        dueDate = new GregorianCalendar(2026, Calendar.MARCH, 22).getTime();
        assignment.setDueDate(dueDate);
        assertFalse(assignment.isOverDue());
    }

    /**
     * tests addSolution Method of Assignment Class
     */
    @Test
    void testAddSolution() {
        Solution solution = new Solution();
        solution.theAuthor = "Sairachana";
        assignment.addSolution(solution);
        assertTrue(assignment.theSolutionList.contains(solution));
    }

    /**
     * tests getSolution Method of Assignment Class
     */
    @Test
    void testGetSolution() {
        Solution solution = new Solution();
        solution.theAuthor = "Sairachana";
        assignment.addSolution(solution);
        assertEquals(solution, assignment.getSolution(solution.theAuthor));
    }

    /**
     * tests getSolution Method of Assignment Class
     */
    @Test
    void testGetSuggestedSolution() {
        Solution solution = new Solution();
        assignment.suggestedSolution = solution;
        assertEquals(assignment.getSuggestedSolution(), solution);
    }

    /**
     * tests getSolutionIterator Method of Assignment Class
     */
    @Test
    void testGetSolutionIterator() {
        assertTrue(assignment.getSolutionIterator() instanceof SolutionIterator);
    }

    /**
     * tests toString Method of Assignment Class
     */
    @Test
    void testToString() {
        assignment.assignmentName = "SER515ASSIGNMENT";
        assertEquals(assignment.toString(), "SER515ASSIGNMENT");
    }

    /**
     * tests getDueDateString Method of Assignment Class
     */
    @Test
    void testGetDueDateString() {
        DateFormat dateFormat = DateFormat.getDateInstance(DateFormat.SHORT);
        assignment.dueDate = new Date();
        assertEquals(assignment.getDueDateString(), dateFormat.format(new Date()));
    }
}
