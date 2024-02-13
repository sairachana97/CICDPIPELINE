package hacs;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 */
public class CourseIteratorTest {

    CourseIterator iterator;
    ClassCourseList courseList;

    @BeforeEach
    void start() {
        courseList = new ClassCourseList();
        courseList.initializeFromFile("CourseInfo.txt");
        iterator = new CourseIterator(courseList);
    }

    /**
     * tests hasnext methos of course iterator class
     */
    @Test
    void testHasNext() {
        assertTrue(iterator.hasNext());
        courseList = new ClassCourseList();
        iterator = new CourseIterator(courseList);
        assertFalse(iterator.hasNext());
    }

    @Test
    void testNext() {
        assertEquals(iterator.next().courseName, "SER515");
        assertEquals(iterator.next().courseName, "SER516");
    }

    @Test
    void testNextNull() {
        courseList = new ClassCourseList();
        iterator = new CourseIterator(courseList);
        assertNull(iterator.next());

    }

    /**
     * tests remove method of class iterator class
     */
    @Test
    void testRemove() {
        int length = iterator.theCourseList.size();
        iterator.remove();
        assertEquals(iterator.theCourseList.size(), length - 1);
    }

    @Test
    void testNextString() {
        assertEquals(iterator.next("SER515").courseName, "SER515");
        assertNull(iterator.next("SER"));
    }

    }

