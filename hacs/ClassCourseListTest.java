package hacs;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Title: HACS Description: SER515 Assignment: UnitTest/Re-use
 * @author Sairachana Paladugu
 * @version 1.0 :: Unit Tests added
 *
 */
public class ClassCourseListTest {
    ClassCourseList classCourseList;

    @BeforeEach
    void start() {

        classCourseList = new ClassCourseList();
    }

    /**
     * tests InitializeFromFile method in ClassCourseList Class
     */
    @Test
    void testInitializeFromFile() {
        classCourseList.initializeFromFile("CourseInfo.txt");
        assertEquals(classCourseList.get(0).courseName, "SER515");
        assertEquals(classCourseList.get(1).courseName, "SER516");
        assertEquals(classCourseList.get(2).courseName, "SER517");
    }

    /**
     * tests findCourseByCourseName method in ClassCourseList Class
     */
    @Test
    void testFindCourseByCourseName() {
        Course course = new Course("SER515", CourseLevel.HighLevel);
        assertEquals(classCourseList.findCourseByCourseName("SER515"), null);
        classCourseList.add(course);
        assertEquals(classCourseList.findCourseByCourseName("SER515"), course);
    }


}

