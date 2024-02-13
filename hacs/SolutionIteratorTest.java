package hacs;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 *
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Test cases
 */
public class SolutionIteratorTest {

    SolutionIterator iterator;
    SolutionList solList;
    Solution sol;

    @BeforeEach
    void start() {
        sol = new Solution();
        solList = new SolutionList();

        sol.theAuthor = "Sairachana";
        sol.solutionFileName = "solution.pdf";
        sol.theGrade = 1;
        sol.reported = true;

        solList.add(sol);
        iterator = new SolutionIterator(solList);
    }

    /**
     * tests hasnext method of solution iterator class
     */
    @Test
    void testHasNext() {
        assertTrue(iterator.hasNext());
        iterator.next();
        assertFalse(iterator.hasNext());
    }

    @Test
    void testNextNull() {
        solList = new SolutionList();
        iterator = new SolutionIterator(solList);
        assertNull(iterator.next());
    }

    /**
     * tests next method of solution iterator class
     */
    @Test
    void testNext() {
        assertEquals(iterator.next().theAuthor, "Sairachana");
        assertNull(iterator.next());
    }

    /**
     * tests remove method of solution iterator class
     */
    @Test
    void testRemove() {
        int length = iterator.solutionList.size();
        iterator.remove();
        assertEquals(iterator.solutionList.size(), length - 1);
    }

    /**
     * tests nextstring method of solutioniterator class
     */
    @Test
    void testNextString() {
        assertEquals(iterator.next("Sairachana").theAuthor, "Sairachana");
        assertNull(iterator.next("Sairachana"));
    }
}
