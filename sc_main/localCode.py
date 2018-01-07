import re

from sc.models import Submission


def processUrl(text):
    # flickr
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    link_type = Submission.LINK_TYPE_NOT_PROCESSED
    regExps = [
        [r'<a data-flickr-embed="true".*<\/script>', Submission.LINK_TYPE_FLICKR, 10, -1],
        [r'<iframe.*src="https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)".*><\/iframe>', Submission.LINK_TYPE_SOUNDCLOUND,
         5, -1],
        [r'[\'"]?([^\'" >]+)youtube([^\'" >]+)', Submission.LINK_TYPE_YOUTUBE],
        [r'<a href=[\'"]?([^\'" >]+)[\'"]>', Submission.LINK_TYPE_NOT_PROCESSED, 9, -1],
    ]
    url = ''
    for i in range(len(regExps)):
        match = re.search(regExps[i][0], text)
        if match:
            url = match.group(0)
            link_type = regExps[i][1]
            if link_type == Submission.LINK_TYPE_YOUTUBE:
                url = url.replace("watch?v=", "embed/")
            elif link_type == Submission.LINK_TYPE_SOUNDCLOUND:
                m = re.search(r'https:\/\/w.soundcloud.com\/[\'"]?([^\'" >]+)', text)
                if m:
                    url = m.group(0)
                else:
                    url = ''
            elif link_type == Submission.LINK_TYPE_FLICKR:
                m = re.search(r'<img src="[\'"]?([^\'" >]+)staticflickr([^\'" >]+)"', text)
                if m:
                    url = m.group(0)[10: -1]
                else:
                    url = ''

            text = re.sub(regExps[i][0], '', text)

    return {'link_type':link_type, 'url':url, 'text':text}
