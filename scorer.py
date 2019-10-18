# CMU 11-785 (Introduction to Deep Learning)
# Final Score Calculator for Homework 1 Part 2 (Kaggle Competition)
# Author: Amit Chahar


import csv
from kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.api_client import ApiClient

regular_dealine_competition_name = '11785-hw1-fall2019'
slack_dealine_competition_name = '11-785-homework-1-part-2-fall-19-slack'
late_deadline_competition_name = '11-785-hw1-fall2019-late'


all_competitions = [regular_dealine_competition_name, slack_dealine_competition_name, late_deadline_competition_name]
api = KaggleApi(ApiClient())
api.authenticate()

def calculate_final_score(public_score, private_score):
    return (0.3 * public_score) + (0.7 * private_score)


for competition in all_competitions:
    submission_data = api.get_competition_submissions_scores(competition, './', 'sample')
    print('teams count: ', len(submission_data))

    with open(competition + '.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        print('teams count: ', len(submission_data))
        csv_writer.writerow(['Team Name', 'Accepted Public Score', 'Accepted Private Score', 'Final Score (0.3*public + 0.7*private)', 'Submission Time (UTC)', 'Total Submissions', 'Submissions Without Error and Before Deadline', 'Individual Submission Scores List [(public, private, calculated),....]'])
        for team_id in submission_data:
            submissions = submission_data[team_id]
            max_score = 0
            team_name = None
            accepted_public_score = None
            accepted_private_score = None
            submission_time = None
            all_scores = []
            for sub in submissions:
                try:
                    if (not sub['isAfterDeadline']) and (sub['status'] != 'error'):
                        public_score = float(sub['publicScore'])
                        private_score = float(sub['privateScore'])
                        calculated_score = calculate_final_score(public_score, private_score)
                        all_scores.append((public_score, private_score, calculated_score))
                        if calculated_score > max_score:
                            team_name = sub['teamName']
                            max_score = calculated_score
                            accepted_public_score = public_score
                            accepted_private_score = private_score
                            submission_time = sub['date']
                except Exception as e:
                    print('Exception: ', e)
                    print('submission: ', sub)


            temp_row = [team_name, accepted_public_score, accepted_private_score, max_score, submission_time, len(submissions), len(all_scores), str(all_scores)]
            csv_writer.writerow(temp_row)
