package hacs;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Iterator;


/**
 * Title:        HACS
 * Description:
 * Copyright:    Copyright (c) 2002
 * Company:      msu
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 *
 */

abstract public class CourseMenu extends JDialog {
  Course theCourse;
  boolean bLogout=true;

  JRadioButton assignmentRadiao = new JRadioButton();
  JComboBox<Assignment> assignmentCombox = new JComboBox<>();
  JButton assignmentViewButton = new JButton();
  JButton assignmentAddButton = new JButton();
  JRadioButton optionRadio = new JRadioButton();
  JLabel assignmentContentLable = new JLabel();
  JComboBox<String> optionCombo = new JComboBox<>();
  JButton optionViewButton = new JButton();
  JButton optionAddButton = new JButton();
  JButton buttonChangeCourse = new JButton();
  JButton buttonLogout = new JButton();

  public CourseMenu() {

    try {
      jbInit();
    } catch(Exception e) {
      e.printStackTrace();
    }
    setModal(true);
    setSize(503,294);
  }

  private void jbInit() throws Exception {
    buttonChangeCourse.setText("ChangeCourse");
    buttonChangeCourse.setBounds(new Rectangle(101, 211, 73, 37));
    buttonChangeCourse.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(ActionEvent e) {
        buttonChangeCourse_actionPerformed(e);
      }
    });
    this.getContentPane().setLayout(null);
    this.setTitle("");
    buttonLogout.setText("Logout");
    buttonLogout.setBounds(new Rectangle(267, 215, 73, 37));
    buttonLogout.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(ActionEvent e) {
        buttonLogout_actionPerformed(e);
      }
    });
    this.getContentPane().add(buttonChangeCourse, null);
    this.getContentPane().add(buttonLogout, null);
  }

  /* when the add button is pressed, call add assignment
  function of facade, after that refresh window
  */

  /* when the add button is pressed, call ViewAssignment
  function of facade, after that refresh window
  */

  abstract void showMenu(Course theCourse);
  abstract void showAddButtons();
  abstract void showViewButtons();
  abstract void showRadios();
  abstract void showComboxes();
  abstract void showLabel();

  void assignmentAddButton_actionPerformed(ActionEvent e) {
    Hacs.theFacade.addAssignment(theCourse);
    refresh();
  }
  void assignmentViewButton_actionPerformed(ActionEvent e) {
    Assignment theAssignment=(Assignment)assignmentCombox.getSelectedItem() ;
    Hacs.theFacade.viewAssignment(theAssignment);
  }
  void refresh() {
    assignmentCombox.removeAllItems() ;
    Iterator<Assignment> Iterator = theCourse.assignmentList.iterator() ;
    while(Iterator.hasNext()) {
      assignmentCombox.addItem(Iterator.next());
    }
  }

  void buttonChangeCourse_actionPerformed(ActionEvent e) {
    bLogout = false;
    setVisible(false);
  }

  void buttonLogout_actionPerformed(ActionEvent e) {
    bLogout = true;
    setVisible(false);
  }
  boolean ifLogout() {
    return bLogout;
  }
}