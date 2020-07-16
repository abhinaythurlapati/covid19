from covid19.lib.objects.tasks.qa import QATask
from covid19.DataManagement.datapreprocessing import DataPreProcessing
from covid19.lib.objects.inverted_index import InvertedIndex
from covid19.DataManagement.loaddata import LoadData
from colorama import Fore, Back, Style
from covid19.lib.objects.researchpaper import ResearchPaper


def question_terms_generator(qa_obj, task_number, concat_sub_task=True):
    if not isinstance(qa_obj, QATask):
        raise TypeError('{} is not of type: {}'.format(qa_obj, QATask))

    qa_obj.load_task(task_num=task_number)
    title = qa_obj.get_current_task_title()

    if not concat_sub_task:
        return DataPreProcessing.clean_text(text=title, remove_char_length=2)
    else:
        for sub_task in qa_obj.get_sub_tasks():
            question_search_text = title + sub_task
            yield DataPreProcessing.clean_text(text=question_search_text, remove_char_length=2)


def highlight_text(text):
    if not isinstance(text, str):
        raise TypeError('kw_arg: "text" is not of type "str"'.format(text))

    return Back.YELLOW + text


if __name__ == "__main__":
    qa_task = QATask()
    task_nums = qa_task.get_tasks(numbers=True)

    for task_num in task_nums:
        search_terms = question_terms_generator(qa_obj=qa_task, task_number=task_num, concat_sub_task=True)
        results_docs_ids = InvertedIndex.get_matching_documents_ids(search_terms=search_terms)
        for doc_id in results_docs_ids:
            research_paper_json = LoadData.get_research_paper_by_id(uid=doc_id)
            rp = ResearchPaper(r_paper=research_paper_json)