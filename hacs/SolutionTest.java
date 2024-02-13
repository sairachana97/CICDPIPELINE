package hacs;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

import static org.junit.Assert.assertEquals;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Test cases
 */
public class SolutionTest {
    Solution solution;

    @BeforeEach
    void start() {
        solution = new Solution();
        solution.theAuthor = "Sairachana";
        solution.solutionFileName = "solution.pdf";
        solution.theGrade = 1;
        solution.reported = true;
    }

    /**
     * tests tostring method of solution class
     */
    @Test
    void testToString() {
        assertEquals(solution.toString(), "Sairachana  solution.pdf Grade=1  reported");
    }

    /**
     * tests getgradestring method of solution class
     */
    @Test
    void testGetGradeString() {
        assertEquals(solution.getGradeString(), "1");
        solution.reported = false;
        assertEquals(solution.getGradeString(), "-1");
    }

    /**
     * tests getgradeint method of solution class
     */
    @Test
    void testGetGradeInt() {
        assertEquals(solution.getGradeInt(), solution.theGrade);
    }

    /**
     * tests isreported method of solution class
     */
    @Test
    void isReported() {
        assertEquals(solution.isReported(), solution.reported);
    }

    @Test
    void getGradeString() {
        assertEquals(solution.getGradeString(), Integer.toString(solution.theGrade));
    }
}
