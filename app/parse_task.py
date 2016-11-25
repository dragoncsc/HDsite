



class process_tasks():

  def parse_tasks(self, from_db ):
    all_tasks = []

    for u in from_db:
      all_tasks.append( ( u.taskname.upper(), u.date, u.type ) )
    return all_tasks






