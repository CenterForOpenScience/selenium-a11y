import os

import pandas as pd
from axe_selenium_python import Axe

import settings


class ApplyA11yRules:
    def run_axe(driver, session, page_name, write_files=True, terminal_errors=True):
        """ Use the axe testing engine to perform accessibility checks on a web page
            Parameters:
            - page_name - string - unique identifier for the web page being tested
                - used as part of file name when writing results files
            - write_files - boolean - used to determine whether or not to write results
                files - default = True
            - terminal_errors - boolean - used to deteremine whether or not to output
                errors to terminal window - default = True
        """
        axe = Axe(driver)
        # Inject axe-core javascript into page.
        axe.inject()
        # Run axe accessibility checks.
        # TODO: Currently applying all axe rules - parammaterize this so that in the
        #       future we can run with more options. (i.e. only WCAG 2A rules, or
        #       excluding Best Practice rules, etc.)
        results = axe.run()
        if write_files:
            write_results_files(axe, results, page_name)
        if terminal_errors:
            # Assert no violations are found
            assert len(results['violations']) == 0, axe.report(results['violations'])


# TODO: Figure out final storage place for results files:
#       Options include:
#       - uploading to OSF Project
#       - shared Google Drive folder
#       - Github repository (either selenium-a11y repo or maybe separate dedicated repo)


def write_results_files(axe, results, page_name):
    """ Write results to output .json files (3 separate files for passes, violations,
    and incomplete) and also convert each .json file to a .csv file.  So there should
    be 6 separate files created for each execution of axe.  We are using the Panda
    library to convert .json to .csv files.
    Parameters:
    - axe - instance of the axe testing engine object
    - results - json object - results object returned from axe containing results of
        accessibility checks. Results are in json format consisting of 4 separate arrays
        (passes, violations, incomplete, and inapplicable)
    - page_name - string - unique identifier for the web page being tested - used as
        part of file name when writing results files
    """
    # Writing all files to a local folder 'a11y_results' to keep them a little more
    # organized
    work_dir = 'a11y_results'
    # Have to first check if the folder exists - if not then create it
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)
    # Files for Passed Rules
    file_name_passes = os.path.join(
        work_dir, 'a11y_' + page_name + '_passes_' + settings.DOMAIN + '.json'
    )
    axe.write_results(results['passes'], file_name_passes)
    pandaObject = pd.read_json(file_name_passes)
    file_name_passes_csv = os.path.join(
        work_dir, 'a11y_' + page_name + '_passes_' + settings.DOMAIN + '.csv'
    )
    pandaObject.to_csv(file_name_passes_csv)
    # Files for Failed Rules (aka Violations)
    file_name_violations = os.path.join(
        work_dir, 'a11y_' + page_name + '_violations_' + settings.DOMAIN + '.json'
    )
    axe.write_results(results['violations'], file_name_violations)
    pandaObject = pd.read_json(file_name_violations)
    file_name_violations_csv = os.path.join(
        work_dir, 'a11y_' + page_name + '_violations_' + settings.DOMAIN + '.csv'
    )
    pandaObject.to_csv(file_name_violations_csv)
    # Files for Rules that couldn't be evaluated by the rules engine (aka Incomplete)
    file_name_incomplete = os.path.join(
        work_dir, 'a11y_' + page_name + '_incomplete_' + settings.DOMAIN + '.json'
    )
    axe.write_results(results['incomplete'], file_name_incomplete)
    pandaObject = pd.read_json(file_name_incomplete)
    file_name_incomplete_csv = os.path.join(
        work_dir, 'a11y_' + page_name + '_incomplete_' + settings.DOMAIN + '.csv'
    )
    pandaObject.to_csv(file_name_incomplete_csv)
