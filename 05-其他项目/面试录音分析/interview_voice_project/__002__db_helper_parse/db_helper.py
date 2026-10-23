from datetime import datetime

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from common.config import Config
from __002__db_helper_parse.model.base import Base
from __002__db_helper_parse.model.tb_interview_recording_analysis import TbInterviewRecordingAnalysis
from __002__db_helper_parse.model.tb_interview_recording_analysis_detail import TbInterviewRecordingAnalysisDetail
from __002__db_helper_parse.model.tb_user import TbUser

conf = Config()


class DatabaseHelper:
    def __init__(self, db_url):
        # 创建数据库引擎
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20, pool_recycle=3600)
        # 创建 Session 类
        Session = sessionmaker(bind=self.engine)
        self.Session = Session
        # 创建所有表
        Base.metadata.create_all(self.engine)

    def get_user_by_id(self, user_id):
        """根据用户ID查询用户信息"""
        session = self.Session()
        try:
            # 查询用户
            user = session.query(TbUser).filter(TbUser.user_id == user_id).first()
            if user:
                return user
            else:
                print(f"没有找到用户ID为 {user_id} 的记录")
                return None
        except Exception as e:
            print(f"查询失败: {e}")
            return None
        finally:
            session.close()

    def add_interview_record(self, name, interview_time=None, company_name=None, recording_url=None, subject=None):
        """初始化添加一条面试记录数据，并返回新添加记录的ID"""
        session = self.Session()
        try:
            # 处理默认值
            if interview_time is None:
                interview_time = datetime.now()  # 默认当前时间
            if company_name is None or company_name == "":
                company_name = "未知公司"  # 默认公司名为 "未知公司"
            if recording_url is None:
                recording_url = ""  # 默认录音地址为空字符串
            if subject is None or subject == "":
                subject = "未知学科"
            processing_status = 0  # 默认处理进度为0（未处理）

            # 创建新记录
            new_record = TbInterviewRecordingAnalysis(
                name=name,
                interview_time=interview_time,
                company_name=company_name,
                recording_url=recording_url,
                processing_status=processing_status,
                subject=subject
            )

            # 添加到数据库
            session.add(new_record)
            session.commit()  # 提交事务

            # 返回新记录的ID
            print(
                f"面试记录已添加: 姓名={name}, 面试时间={interview_time}, 公司={company_name}, 录音地址={recording_url}")
            return new_record.id  # 返回新记录的id
        except Exception as e:
            print(f"添加面试记录失败: {e}")
            session.rollback()  # 出现异常时回滚事务
            return None
        finally:
            session.close()

    def update_interview_record(self, record_id, update_fields):
        if not record_id:
            print("面试记录ID不能为空")
            return
        """根据ID修改指定字段"""
        session = self.Session()
        try:
            # 根据ID查找面试记录
            record = session.query(TbInterviewRecordingAnalysis).filter(
                TbInterviewRecordingAnalysis.id == record_id).first()

            if record:
                # 遍历传入的字段字典并修改对应字段
                for field, value in update_fields.items():
                    if hasattr(record, field):  # 确保字段存在
                        setattr(record, field, value)
                    else:
                        print(f"字段 {field} 不存在于面试记录中")

                # 提交修改
                session.commit()
                print(f"面试记录ID={record_id} 已更新")
            else:
                print(f"未找到ID为 {record_id} 的面试记录")
        except Exception as e:
            print(f"更新面试记录失败: {e}")
            session.rollback()  # 出现异常时回滚事务
        finally:
            session.close()

    def get_all_interview_records(self, filters=None, exclude_fields=None):
        """查询所有面试记录，支持根据条件过滤，并返回字典格式，按修改时间倒序排序"""
        session = self.Session()
        try:
            # 查询所有记录
            query = session.query(TbInterviewRecordingAnalysis)

            # 如果传入了过滤条件，应用这些条件
            if filters:
                query = query.filter_by(**filters)

            # 如果指定了排除字段，使用 with_entities 来指定返回的字段
            if exclude_fields:
                # 获取模型中的所有字段名
                all_columns = [column.name for column in TbInterviewRecordingAnalysis.__table__.columns]
                # 排除指定的字段
                included_columns = [column for column in all_columns if column not in exclude_fields]
                # 使用 with_entities 来选择需要的字段
                query = query.with_entities(*[getattr(TbInterviewRecordingAnalysis, col) for col in included_columns])

            # 按修改时间倒序排序
            query = query.order_by(desc(TbInterviewRecordingAnalysis.update_time))

            records = query.all()

            if records:
                # 将查询结果转换为字典格式
                records_dict = [record._asdict() if hasattr(record, '_asdict') else record.__dict__ for record in
                                records]

                # 去除 SQLAlchemy 的内置属性 '_sa_instance_state'
                for record in records_dict:
                    record.pop('_sa_instance_state', None)

                return records_dict
            else:
                print("没有找到任何面试记录")
                return []
        except Exception as e:
            print(f"查询面试记录失败: {e}")
            return []
        finally:
            session.close()

    def add_interview_analysis_detail(self, interview_record_analysis_id, interview_question=None,
                                      interviewee_answer=None,
                                      reference_answer=None, point_analysis=None, answer_thoughts=None,
                                      answer_evaluation=None, answer_score=None):
        """添加一条面试记录分析详细数据"""
        if not interview_record_analysis_id:
            print("面试记录分析ID不能为空")
            return
        session = self.Session()
        try:
            # 创建新记录
            new_detail = TbInterviewRecordingAnalysisDetail(
                interview_record_analysis_id=interview_record_analysis_id,
                interview_question=interview_question,
                interviewee_answer=interviewee_answer,
                reference_answer=reference_answer,
                point_analysis=point_analysis,
                answer_thoughts=answer_thoughts,
                answer_evaluation=answer_evaluation,
                answer_score=answer_score
            )

            # 添加到数据库
            session.add(new_detail)
            session.commit()  # 提交事务

            print(f"面试记录分析详情已添加: 面试问题={interview_question}, 面试者回答={interviewee_answer}")
        except Exception as e:
            print(f"添加面试记录分析详情失败: {e}")
            session.rollback()  # 出现异常时回滚事务
        finally:
            session.close()

    def get_analysis_details_by_record_id(self, interview_record_analysis_id):
        """根据 interview_record_analysis_id 查询所有面试记录分析详情"""
        session = self.Session()
        try:
            # 查询所有匹配的分析记录
            details = session.query(TbInterviewRecordingAnalysisDetail).filter(
                TbInterviewRecordingAnalysisDetail.interview_record_analysis_id == interview_record_analysis_id).all()

            if details:
                # 将查询结果转换为字典格式
                details_dict = [detail.__dict__ for detail in details]

                # 去除 SQLAlchemy 的内置属性 '_sa_instance_state'
                for detail in details_dict:
                    detail.pop('_sa_instance_state', None)

                return details_dict
            else:
                print(f"未找到与分析ID {interview_record_analysis_id} 相关的面试记录分析详情")
                return []
        except Exception as e:
            print(f"查询面试记录分析详情失败: {e}")
            return []
        finally:
            session.close()

    def delete_analysis_details_by_record_id(self, record_id):
        """根据面试记录分析ID删除面试记录分析详情"""
        if not record_id:
            print("面试记录分析ID不能为空")
            return
        session = self.Session()
        try:
            # 删除 tb_interview_recording_analysis_detail 表中的所有相关记录
            deleted_count = session.query(TbInterviewRecordingAnalysisDetail).filter(
                TbInterviewRecordingAnalysisDetail.interview_record_analysis_id == record_id).delete()

            # 提交事务
            session.commit()

            if deleted_count > 0:
                print(f"面试记录分析ID={record_id} 的所有分析详情已删除")
            else:
                print(f"未找到与分析ID {record_id} 相关的分析详情")
        except Exception as e:
            print(f"删除面试记录分析详情失败: {e}")
            session.rollback()  # 出现异常时回滚事务
        finally:
            session.close()


def get_db_helper(host, user_name, password, db_name):
    database_url = f"mysql+pymysql://{user_name}:{password}@{host}/{db_name}"
    db_helper = DatabaseHelper(database_url)
    return db_helper


my_db_helper = get_db_helper(conf.MYSQL_HOST, conf.MYSQL_USER, conf.MYSQL_PASSWORD, conf.MYSQL_DATABASE_NAME)

if __name__ == "__main__":
    # 添加面试记录
    # my_db_helper.add_interview_record("张三", company_name="百度", recording_url="")
    # 修改面试记录
    # my_db_helper.update_interview_record(1, {"name": "王五", "company_name": "腾讯"})
    # 查询所有的记录
    records = my_db_helper.get_all_interview_records(exclude_fields=["markdown_text"])
    print(records)
    # 添加详细记录
    # 假设已有db_helper实例
    # my_db_helper.add_interview_analysis_detail(
    #     interview_record_analysis_id=1,
    #     interview_question="请介绍一下自己",
    #     interviewee_answer="我是一名软件工程师...",
    #     reference_answer="面试官期望的答案...",
    #     point_analysis="分析该问题的关键点...",
    #     answer_thoughts="答题的思路...",
    #     answer_evaluation="回答整体评价...",
    #     answer_score=85.5
    # )
    # 根据id进行查询
    # details = my_db_helper.get_analysis_details_by_record_id(1)
    # print(details)
    # 测试下get_all_interview_records的filter
    # records = my_db_helper.get_all_interview_records(filters={"name": "张三"})
