from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError


class ResearchPaper:
    """
    Provides various functions on an object
    """

    def __init__(self, r_paper, schema=None):
        if not isinstance(r_paper, dict):
            raise TypeError('Argument is not of type "type"')
        else:
            self.r_paper = r_paper
            self.schema = schema

    def validate_schema(self):
        try:
            json_validate(instance=self.r_paper, schema=self.schema)
            return True
        except ValidationError as e:
            return False

    def has_paper_id(self):
        paper_id = self.r_paper.get('paper_id')
        if paper_id != '' or len(paper_id) > 0:
            return True
        else:
            return False

    def has_title(self):
        title = self.r_paper.get('metadata', {}).get('title')
        if title != '' or len(title) > 0:
            return True
        else:
            return False

    def has_abstract(self):
        abstract = self.r_paper.get('Abstract', [])
        if len(abstract) > 0 and isinstance(abstract, list) and len(abstract['text']) > 0:
            return True
        else:
            return False

    def has_body_text(self):
        body_text = self.r_paper.get('body_text', {})
        if len(body_text) > 0 and isinstance(body_text, list) and len(body_text) > 0:
            return True
        else:
            return False

    def get_r_paper_id(self):
        """
        returns the research paper id
        :return:
        """
        return self.r_paper.get('paper_id', {}) if self.has_paper_id() else None

    def get_r_paper_title(self):
        """
        returns the text of the research paper if title has content
        :return:
        """
        return self.r_paper.get('metadata', {}).get('title') if self.has_title() else ''

    def get_abstract(self):
        """
        concats the abstract to single paragraph if it spans more than one paragraph and returns the text
        returns the empty list other wise
        :return:
        """
        abstract = self.r_paper.get('Abstract')
        abstract_text = ''
        if self.has_abstract():
            for abstract_para in abstract:
                abstract_text += abstract_para['text']

        return abstract_text

    def format_body(self, field="text"):
        """
        returns a list of body text headers
        :return:
        """
        allowed_field_strings = ["text", "section"]
        if field not in allowed_field_strings:
            raise ValueError('kw_arg "field" is not one of the {}'.format(','.join(allowed_field_strings)))

        body_text_list = self.r_paper.get('body_text', {})
        body_text_set = set()
        if self.has_body_text():
            for body_text in body_text_list:
                body_text_set.add(body_text.get(field))
        return list(body_text_set)

    def get_all_sentences(self, exclude_fields=None):
        """
        returns the list of all the sentences from the following
        1) Title of the research paper
        2) Abstract content
        3) Body Text content
        4) Headings of body text content
        :return: list of all sentences
        """

        allowed_exclude_fields = set(['title', 'abstract', 'body_text', 'body_headers'])

        if isinstance(exclude_fields, str) and exclude_fields is not None:
            if exclude_fields not in allowed_exclude_fields:
                raise ValueError('kw_arg "exclude_fields" should be one of {}'.format(allowed_exclude_fields))

        if exclude_fields is not None and (not isinstance(exclude_fields, list) or not set(exclude_fields).issubset(allowed_exclude_fields)):
            raise ValueError('kw_arg "exclude_fields" can contain {}'.format(allowed_exclude_fields))

        if exclude_fields is None:
            exclude_fields = set([])

        fields_to_include = allowed_exclude_fields.difference(exclude_fields)
        full_text = list()

        if 'title' in fields_to_include:
            title = self.get_r_paper_title()
            if title != '':
                full_text.extend(title)

        if 'abstract' in fields_to_include:
            abstract = self.get_abstract()
            if abstract != '':
                full_text.extend(abstract)

        if 'body_text' in fields_to_include:
            body_text = self.format_body(field='text')
            if body_text != '':
                full_text.extend(body_text)

        if 'body_headers' in fields_to_include:
            body_headers = self.format_body(field='section')
            if body_headers != '':
                full_text.extend(body_headers)

        return full_text

    def generate_authors_dict(self):
        """
        generates a dict of all authors asscocited with a research paper
        :return:
        """

        pass


    @staticmethod
    def format_authors_name(authors_names):
        """
        formats the authors name to space separated entity i.e 'f_name m_name l_name suffix'
        :return: list of formatted names
        """
        if not isinstance(authors_names, list):
            raise TypeError('kw_arg: "authors_name is not of type list"')
        authors_names = list()
        for author_dict in authors_names:
            author_name = ''
            if author_dict['first']:
                author_name += author_dict['first']
            if author_dict['middle']:
                author_name += ' '.join(author_dict['middle'])
            if author_dict['last']:
                author_name += author_dict['last']
            if author_dict['suffix']:
                author_name += author_dict['suffix']

            authors_names.append(author_name)
        return authors_names

