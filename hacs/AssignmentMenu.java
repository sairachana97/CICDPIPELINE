package hacs;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;


/**
 * Title:        HACS
 * Description:
 * Copyright:    Copyright (c) 2002
 * Company:      msu
 * @author Zhang ji Zhu Wei
 * @version 1.0
 * @author Sairachana Paladugu
 * @version 2.0 :: Update Code to 2021 Standards
 */

abstract public class AssignmentMenu extends JDialog {
  abstract void showMenu(Assignment assignment,Person person);
  public AssignmentMenu() {
    setModal(true);
    setSize(575,330);
  }
}