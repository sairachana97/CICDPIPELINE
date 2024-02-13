package hacs;

/**
 * Title: HACS Description: Copyright: Copyright (c) 2002 Company: msu
 * 
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author mjfindler
 * @version 2.0 Update to Java 8
 * @author Sairachana Paladugu
 * @version 3.0 :: Update Code to 2021 Standards
 */

public class Hacs {

	static Facade theFacade = new Facade();

	public Hacs() {
	}

	/**
	 * Main function for this project
	 *
	 * @param args
	 */
	public static void main(String[] args) {
		UserInfoItem userInfoItem = new UserInfoItem();
		theFacade.createCourseList();
		while (true) {
			boolean bExit = false;
			bExit = Facade.login(userInfoItem);
			if (bExit)
				break;
			// userinfoitem.strUserName = "Inst1";
			// userinfoitem.UserType = 1;
			theFacade.createUser(userInfoItem);
			theFacade.attachCourseToUser();
			if (userInfoItem.userType == UserType.Student) // if is a student remind him of the due date
				theFacade.remind();
			boolean bLogout = false;
			while (!bLogout) {
				bLogout = theFacade.selectCourse();
				if (bLogout)
					break;
				bLogout = theFacade.courseOperation();
			}
		}
		//    System.out.println(userinfoitem.strUserName +userinfoitem.UserType );
	}
}