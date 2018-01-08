import re

from sc.models import Submission


def processUrl(text):
    # flickr
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    link_type = Submission.LINK_TYPE_NOT_PROCESSED
    regExps = [
        [r'<iframe.*src="https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)".*><\/iframe>', Submission.LINK_TYPE_SOUNDCLOUND],
        [r'<[\'"]?([^\'" >]+)youtube([^\'" >]+)>', Submission.LINK_TYPE_YOUTUBE],
        [r'<a href=[\'"]?([^\'" >]+)[\'"]>', Submission.LINK_TYPE_NOT_PROCESSED],
    ]
    url = ''
    for i in range(len(regExps)):
        match = re.search(regExps[i][0], text)
        if match:
            url = match.group(0)
            link_type = regExps[i][1]
            if link_type == Submission.LINK_TYPE_YOUTUBE:
                url = url.replace("watch?v=", "embed/")[1:-1]
            elif link_type == Submission.LINK_TYPE_SOUNDCLOUND:
                m = re.search(r'https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)', url)
                if m:
                    url = m.group(0)
                else:
                    url = ''
            elif link_type == Submission.LINK_TYPE_NOT_PROCESSED:
                url = url[10:-2]

            text = re.sub(regExps[i][0], '', text)

    return {'link_type':link_type, 'url':url, 'text':text}
