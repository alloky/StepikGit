import argparse
import os

from api import StepikAdapter
from course_struct import Course

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='root_path', action="store", default=".")


def main():
    args = parser.parse_args()
    path = args.root_path
    course_id = 48474

    client_id = "ZUTgBY9yDUn2fnRR16z7bNQl0f3C9euqhVe8pSou"
    client_secret = "z82Rr6Y7Jc99ERvVZJoIyxNqG6bPgQRUbR9yHTtt1msPwAR513KcaduRLDASq9dwadgIm5GVO2kd5m79jZNktsFZdUrp3TGHiXPiA5XwTnRRLfnFrfwnTrYw9dC3P6q0"

    stpk_adapter = StepikAdapter(client_id, client_secret)
    stpk_adapter.clone_course(path, course_id)
    course = Course(path)
    # course.push()

main()

