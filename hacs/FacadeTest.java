package hacs;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

/**
 * Title:HACS Description:SER515 Assignment:UnitTest/Re-use
 * @author Sairachana Paladugu
 * @version 1.0::Unit Tests added
 *
 */
public class FacadeTest {

    Facade facade;

    @BeforeEach
    void start() {
        facade = new Facade();
    }

    /**
     * This method tests reportSolutions method in Facade class
     */
    @Test
    void testReportSolutions() {
        Assignment assignment = new Assignment();
        assignment.theSolutionList.add(new Solution());
        facade.reportSolutions(assignment);
        assertTrue(assignment.theSolutionList.get(0).reported);
    }

    /**
     * This method tests  submitSolutions method in Facade class
     */
    @Test
    void testSubmitSolution() {
        Assignment assignment = new Assignment();
        Solution solution = new Solution();
        facade.submitSolution(assignment, solution);
        assertTrue(assignment.theSolutionList.contains(solution));
    }

    /**
     * This method tests createUser method of Facade class
     */
    @Test
    void testCreateUser() {
        UserInfoItem user = new UserInfoItem();

        user.strUserName = "MFindler";
        user.userType = UserType.Instructor;
        facade.createUser(user);
        assertEquals(facade.thePerson.userName, "MFindler");

        user.strUserName = "Sairachana";
        user.userType = UserType.Student;
        facade.createUser(user);
        assertEquals(facade.thePerson.userName, "Sairachana");
    }

    /**
     * This method test create usertype method of Facade class for student and Instructor
     */
    @Test
    void testCreateUserType() {
        UserInfoItem user = new UserInfoItem();
        user.strUserName = "Sairachana";
        user.userType = UserType.Student;
        facade.createUser(user);
        assertTrue(facade.thePerson instanceof Student);

        user.strUserName = "Findler";
        user.userType = UserType.Instructor;
        facade.createUser(user);
        assertTrue(facade.thePerson instanceof Instructor);
    }

    /**
     * This method tests createCourseList method in Facade class
     */
    @Test
    void testCreateCourseList() {
        facade.createCourseList();
        assertEquals(facade.theCourseList.size(), 3);
    }

    /**
     * This method tests attachcoursetouser method of Facade class
     */
    @Test
    void testAttachCourseToUser() {
        facade.thePerson = new Student();
        facade.thePerson.userName = "tutu";
        facade.createCourseList();
        facade.attachCourseToUser();
        assertEquals(facade.thePerson.courseList.get(1).courseName, "SER516");
    }





}
