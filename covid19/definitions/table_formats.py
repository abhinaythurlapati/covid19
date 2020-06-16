from covid19.definitions.columns import Columns

class BaseColumns:

    @staticmethod
    def columns():
        columns_list = list()
        columns_list.append(Columns.date)
        columns_list.append(Columns.study)
        columns_list.append(Columns.study_link)
        columns_list.append(Columns.journal)
        columns_list.append(Columns.study_type)
        columns_list.append(Columns.added_on)
        columns_list.append(Columns.doi)
        columns_list.append(Columns.cord_uid)


class Format1(BaseColumns):
    name = 'Population'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.adressed_population)
        columns_list.extend(Columns.challenge)
        columns_list.extend(Columns.solution)
        columns_list.extend(Columns.measure_of_evidence)


class Format2(BaseColumns):
    name = 'Relevant Factors'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.factors)
        columns_list.extend(Columns.influential)
        columns_list.extend(Columns.excerpt)
        columns_list.extend(Columns.measure_of_evidence)


class Format3(BaseColumns):
    name = 'Patient Descriptions'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.sample_size)
        columns_list.extend(Columns.age)
        columns_list.extend(Columns.sample_obtained)
        columns_list.extend(Columns.asymptomatic)
        columns_list.extend(Columns.excerpt)


class Format4(BaseColumns):
    name = 'Models and Open Questions'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.method)
        columns_list.extend(Columns.result)
        columns_list.extend(Columns.measure_of_evidence)



class Format5(BaseColumns):
    name = 'Materials'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.material)
        columns_list.extend(Columns.method)
        columns_list.extend(Columns.days_after_onset)
        columns_list.extend(Columns.property2)
        columns_list.extend(Columns.conclusion)
        columns_list.extend(Columns.measure_of_evidence)


class Format6(BaseColumns):
    name = 'Diagnostics'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.detection_method)
        columns_list.extend(Columns.sample)
        columns_list.extend(Columns.obtained_sample)
        columns_list.extend(Columns.measure_of_evidence)
        columns_list.extend(Columns.speed_of_assay)
        columns_list.extend(Columns.fda_approval)


class Format7(BaseColumns):
    name = 'Therapetics, interventions and clinical trails'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.therapeutic_method)
        columns_list.extend(Columns.sample)
        columns_list.extend(Columns.severity_of_symptoms)
        columns_list.extend(Columns.general_outcome)
        columns_list.extend(Columns.primary_endpoint_study)
        columns_list.extend(Columns.clinical_improvement)


class Format8(BaseColumns):
    name = 'Risk Factors'

    @staticmethod
    def columns():
        columns_list = BaseColumns.columns()
        columns_list.extend(Columns.severity_of_disease)
        columns_list.extend(Columns.severity_lower_bound)
        columns_list.extend(Columns.severity_upper_bound)
        columns_list.extend(Columns.severity_p_value)
        columns_list.extend(Columns.severe_significance)
        columns_list.extend(Columns.severe_adjusted)
        columns_list.extend(Columns.hand_calculated_severe)
        columns_list.extend(Columns.fatality)
        columns_list.extend(Columns.fatality_lower_bound)
        columns_list.extend(Columns.fatality_upper_bound)
        columns_list.extend(Columns.fatality_p_value)
        columns_list.extend(Columns.fatality_significance)
        columns_list.extend(Columns.fatality_adjusted)
        columns_list.extend(Columns.hand_calculated_fatality)
        columns_list.extend(Columns.multivariate_adjustment)
        columns_list.extend(Columns.sample_size)
        columns_list.extend(Columns.study_population)


