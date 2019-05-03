import app
from constants import Thresholds

test = Thresholds()
test.comment, test.submission, test.pm = (0, 0, 0)

app.main(test)
