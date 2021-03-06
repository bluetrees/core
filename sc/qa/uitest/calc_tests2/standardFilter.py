# -*- tab-width: 4; indent-tabs-mode: nil; py-indent-offset: 4 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from uitest.framework import UITestCase
from uitest.uihelper.common import get_state_as_dict
from uitest.uihelper.common import select_pos
from uitest.uihelper.calc import enter_text_to_cell
from libreoffice.calc.document import get_cell_by_position
from libreoffice.uno.propertyvalue import mkPropertyValues
# import org.libreoffice.unotest
# import pathlib
from uitest.path import get_srcdir_url
#Bug 113979 - Paste unformatted text does not ignore empty cells
def get_url_for_data_file(file_name):
#    return pathlib.Path(org.libreoffice.unotest.makeCopyFromTDOC(file_name)).as_uri()
    return get_srcdir_url() + "/sc/qa/uitest/calc_tests/data/" + file_name

class standardFilter(UITestCase):
    def test_standard_filter(self):
        calc_doc = self.ui_test.load_file(get_url_for_data_file("standardFilter.ods"))
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:C8"}))

        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xconnect2 = xDialog.getChild("connect2")
        xfield2 = xDialog.getChild("field2")
        xval2 = xDialog.getChild("val2")

        props = {"TEXT": "a"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"1"}))
        propsA = {"TEXT": "OR"}
        actionPropsA = mkPropertyValues(propsA)
        xconnect2.executeAction("SELECT", actionPropsA)
        props2 = {"TEXT": "b"}
        actionProps2 = mkPropertyValues(props2)
        xfield2.executeAction("SELECT", actionProps2)
        xval2.executeAction("TYPE", mkPropertyValues({"TEXT":"3"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #3x down - should be on row 9
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "8")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xconnect2 = xDialog.getChild("connect2")
        xfield2 = xDialog.getChild("field2")
        xval2 = xDialog.getChild("val2")

        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "a")
        self.assertEqual(get_state_as_dict(xfield2)["SelectEntryText"], "b")
        self.assertEqual(get_state_as_dict(xconnect2)["SelectEntryText"], "OR")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "1")
        self.assertEqual(get_state_as_dict(xval2)["Text"], "3")
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        self.ui_test.close_doc()

    def test_standard_filter_copy_result(self):
        calc_doc = self.ui_test.load_file(get_url_for_data_file("standardFilter.ods"))
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:C8"}))

        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xconnect2 = xDialog.getChild("connect2")
        xfield2 = xDialog.getChild("field2")
        xval2 = xDialog.getChild("val2")
        xcopyresult = xDialog.getChild("copyresult")
        xedcopyarea = xDialog.getChild("edcopyarea")
        props = {"TEXT": "a"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"1"}))
        propsA = {"TEXT": "OR"}
        actionPropsA = mkPropertyValues(propsA)
        xconnect2.executeAction("SELECT", actionPropsA)
        props2 = {"TEXT": "b"}
        actionProps2 = mkPropertyValues(props2)
        xfield2.executeAction("SELECT", actionProps2)
        xval2.executeAction("TYPE", mkPropertyValues({"TEXT":"3"}))
        xcopyresult.executeAction("CLICK", tuple())
        xedcopyarea.executeAction("TYPE", mkPropertyValues({"TEXT":"F1"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #verify
        self.assertEqual(get_cell_by_position(document, 0, 5, 0).getString(), "a")
        self.assertEqual(get_cell_by_position(document, 0, 6, 0).getString(), "b")
        self.assertEqual(get_cell_by_position(document, 0, 7, 0).getString(), "c")
        self.assertEqual(get_cell_by_position(document, 0, 5, 1).getValue(), 1)
        self.assertEqual(get_cell_by_position(document, 0, 6, 1).getValue(), 2)
        self.assertEqual(get_cell_by_position(document, 0, 7, 1).getValue(), 3)
        self.assertEqual(get_cell_by_position(document, 0, 5, 2).getValue(), 2)
        self.assertEqual(get_cell_by_position(document, 0, 6, 2).getValue(), 3)
        self.assertEqual(get_cell_by_position(document, 0, 7, 2).getValue(), 4)
        self.ui_test.close_doc()

    def test_standard_filter_copy_result_next_sheet(self):
        calc_doc = self.ui_test.load_file(get_url_for_data_file("standardFilter.ods"))
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:C8"}))

        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xconnect2 = xDialog.getChild("connect2")
        xfield2 = xDialog.getChild("field2")
        xval2 = xDialog.getChild("val2")
        xcopyresult = xDialog.getChild("copyresult")
        xedcopyarea = xDialog.getChild("edcopyarea")
        props = {"TEXT": "a"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"1"}))
        propsA = {"TEXT": "OR"}
        actionPropsA = mkPropertyValues(propsA)
        xconnect2.executeAction("SELECT", actionPropsA)
        props2 = {"TEXT": "b"}
        actionProps2 = mkPropertyValues(props2)
        xfield2.executeAction("SELECT", actionProps2)
        xval2.executeAction("TYPE", mkPropertyValues({"TEXT":"3"}))
        xcopyresult.executeAction("CLICK", tuple())
        xedcopyarea.executeAction("TYPE", mkPropertyValues({"TEXT":"$Sheet2.$F$1"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #verify
        self.assertEqual(get_cell_by_position(document, 1, 5, 0).getString(), "a")
        self.assertEqual(get_cell_by_position(document, 1, 6, 0).getString(), "b")
        self.assertEqual(get_cell_by_position(document, 1, 7, 0).getString(), "c")
        self.assertEqual(get_cell_by_position(document, 1, 5, 1).getValue(), 1)
        self.assertEqual(get_cell_by_position(document, 1, 6, 1).getValue(), 2)
        self.assertEqual(get_cell_by_position(document, 1, 7, 1).getValue(), 3)
        self.assertEqual(get_cell_by_position(document, 1, 5, 2).getValue(), 2)
        self.assertEqual(get_cell_by_position(document, 1, 6, 2).getValue(), 3)
        self.assertEqual(get_cell_by_position(document, 1, 7, 2).getValue(), 4)
        self.ui_test.close_doc()

    def test_standard_filter_case_sensitive(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "first")
        enter_text_to_cell(gridwin, "B1", "second")
        enter_text_to_cell(gridwin, "A2", "a1")
        enter_text_to_cell(gridwin, "A3", "A1")
        enter_text_to_cell(gridwin, "A4", "A1")
        enter_text_to_cell(gridwin, "B2", "4")
        enter_text_to_cell(gridwin, "B3", "5")
        enter_text_to_cell(gridwin, "B4", "6")
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:B4"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcase = xDialog.getChild("case")

        props = {"TEXT": "first"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"a1"}))
        xcase.executeAction("CLICK", tuple())
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #2x down - should be on row 5
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "4")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcase = xDialog.getChild("case")

        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "first")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "a1")
        self.assertEqual(get_state_as_dict(xcase)["Selected"], "true")
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        self.ui_test.close_doc()

    def test_standard_filter_regular_expression(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "first")
        enter_text_to_cell(gridwin, "B1", "second")
        enter_text_to_cell(gridwin, "A2", "aa")
        enter_text_to_cell(gridwin, "A3", "aaa")
        enter_text_to_cell(gridwin, "A4", "abbb")
        enter_text_to_cell(gridwin, "A5", "accc")
        enter_text_to_cell(gridwin, "A6", "a*")
        enter_text_to_cell(gridwin, "B2", "1")
        enter_text_to_cell(gridwin, "B3", "2")
        enter_text_to_cell(gridwin, "B4", "3")
        enter_text_to_cell(gridwin, "B5", "4")
        enter_text_to_cell(gridwin, "B6", "5")
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:B6"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xregexp = xDialog.getChild("regexp")

        props = {"TEXT": "first"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"a*"}))
        xregexp.executeAction("CLICK", tuple())
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #3x down - should be on row 7
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "6")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xregexp = xDialog.getChild("regexp")

        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "first")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "a*")
        self.assertEqual(get_state_as_dict(xregexp)["Selected"], "true")
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        self.ui_test.close_doc()

    def test_standard_filter_condition_contains(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "first")
        enter_text_to_cell(gridwin, "B1", "second")
        enter_text_to_cell(gridwin, "A2", "aa")
        enter_text_to_cell(gridwin, "A3", "aaa")
        enter_text_to_cell(gridwin, "A4", "abbb")
        enter_text_to_cell(gridwin, "A5", "accc")
        enter_text_to_cell(gridwin, "A6", "a*")
        enter_text_to_cell(gridwin, "B2", "1")
        enter_text_to_cell(gridwin, "B3", "2")
        enter_text_to_cell(gridwin, "B4", "3")
        enter_text_to_cell(gridwin, "B5", "4")
        enter_text_to_cell(gridwin, "B6", "5")
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:B6"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xregexp = xDialog.getChild("regexp")

        props = {"TEXT": "first"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"a*"}))
        xregexp.executeAction("CLICK", tuple())
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        #3x down - should be on row 7
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "6")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xregexp = xDialog.getChild("regexp")

        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "first")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "a*")
        self.assertEqual(get_state_as_dict(xregexp)["Selected"], "true")
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)
        self.ui_test.close_doc()

        #from testcasespecification OOo
    def test_standard_filter_condition_contains2(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Contains"/Enter value "cio"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Contains"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"cio"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,3, 4 are visible (2 and 5 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "2")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "3")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "cio")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Contains")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)
        self.ui_test.close_doc()

    def test_standard_filter_condition_does_not_contains(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Does not contain"/Enter value "cio"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Does not contain"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"cio"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,2, 5 are visible (3 and 4 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "1")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "4")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "cio")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Does not contain")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)

        self.ui_test.close_doc()

    def test_standard_filter_condition_Begins_with(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Begins with"/Enter value "si"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Begins with"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"so"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,3, 4 are visible (2 and 5 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "2")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "3")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "so")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Begins with")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)

        self.ui_test.close_doc()

    def test_standard_filter_condition_Does_not_begin_with(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Does not contain"/Enter value "cio"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Does not begin with"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"so"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,2, 5 are visible (3 and 4 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "1")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "4")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "so")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Does not begin with")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)

        self.ui_test.close_doc()

    def test_standard_filter_condition_Ends_with(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Does not contain"/Enter value "cio"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Ends with"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"s"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,2, 5 are visible (3 and 4 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "1")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "4")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "s")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Ends with")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)

        self.ui_test.close_doc()

    def test_standard_filter_condition_Does_not_end_with(self):
        calc_doc = self.ui_test.create_doc_in_start_center("calc")
        xCalcDoc = self.xUITest.getTopFocusWindow()
        gridwin = xCalcDoc.getChild("grid_window")
        document = self.ui_test.get_component()

        enter_text_to_cell(gridwin, "A1", "A")
        enter_text_to_cell(gridwin, "B1", "B")
        enter_text_to_cell(gridwin, "C1", "C")
        enter_text_to_cell(gridwin, "D1", "D")
        enter_text_to_cell(gridwin, "A2", "economics")
        enter_text_to_cell(gridwin, "B2", "34")
        enter_text_to_cell(gridwin, "C2", "67")
        enter_text_to_cell(gridwin, "D2", "122")
        enter_text_to_cell(gridwin, "A3", "socioeconomic")
        enter_text_to_cell(gridwin, "B3", "45")
        enter_text_to_cell(gridwin, "C3", "77")
        enter_text_to_cell(gridwin, "D3", "333")
        enter_text_to_cell(gridwin, "A4", "sociology")
        enter_text_to_cell(gridwin, "B4", "78")
        enter_text_to_cell(gridwin, "C4", "89")
        enter_text_to_cell(gridwin, "D4", "56")
        enter_text_to_cell(gridwin, "A5", "humanities")
        enter_text_to_cell(gridwin, "B5", "45")
        enter_text_to_cell(gridwin, "C5", "67")
        enter_text_to_cell(gridwin, "D5", "89")
        #Select
        gridwin.executeAction("SELECT", mkPropertyValues({"RANGE": "A1:D5"}))
        #Choose DATA-FILTER-STANDARDFILTER
        #Choose field name "A"/ Choose condition "Begins with"/Enter value "si"/Press OK button
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")

        props = {"TEXT": "A"}
        actionProps = mkPropertyValues(props)
        xfield1.executeAction("SELECT", actionProps)
        props2 = {"TEXT": "Does not end with"}
        actionProps2 = mkPropertyValues(props2)
        xcond1.executeAction("SELECT", actionProps2)
        xval1.executeAction("TYPE", mkPropertyValues({"TEXT":"s"}))
        xOKBtn = xDialog.getChild("ok")
        self.ui_test.close_dialog_through_button(xOKBtn)

        #Verify that row 1,3, 4 are visible (2 and 5 are hidden)
        gridwin.executeAction("SELECT", mkPropertyValues({"CELL": "A1"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "2")
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "DOWN"}))
        gridWinState = get_state_as_dict(gridwin)
        self.assertEqual(gridWinState["CurrentRow"], "3")
        #reopen filter and verify
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        gridwin.executeAction("TYPE", mkPropertyValues({"KEYCODE": "UP"}))
        self.ui_test.execute_modeless_dialog_through_command(".uno:DataFilterStandardFilter")
        xDialog = self.xUITest.getTopFocusWindow()
        xfield1 = xDialog.getChild("field1")
        xval1 = xDialog.getChild("val1")
        xcond1 = xDialog.getChild("cond1")
        self.assertEqual(get_state_as_dict(xfield1)["SelectEntryText"], "A")
        self.assertEqual(get_state_as_dict(xval1)["Text"], "s")
        self.assertEqual(get_state_as_dict(xcond1)["SelectEntryText"], "Does not end with")
        xCancelBtn = xDialog.getChild("cancel")
        self.ui_test.close_dialog_through_button(xCancelBtn)

        self.ui_test.close_doc()
# vim: set shiftwidth=4 softtabstop=4 expandtab:
