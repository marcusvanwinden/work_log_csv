<h1>Work Log CSV</h1>

<br>

<h2>Table of Contents</h2>
<ol>
  <li><a href="#description">Description</a></li>
  <li><a href="#installation">Installation</a></li>
</ol>

<br>

<h2 id="description">1. Description</h2>
<p>To prepare better timesheets for a company, I developed a terminal application for logging what work someone did on a certain day. The script asks for a task name, how much time was spent on the task, and any general notes about the task. The program records each of these items into a row of a CSV file along with a date. I also provided a way for a user to find all of the tasks that were done on a certain date or that match a search string.</p>

<table>
  <tr>
    <th>Main Menu</th>
    <th>Add New Entry</th>
  </tr>
  <tr>
    <td><img src="assets/main_menu.png" width=500></td>
    <td><img src="assets/add_entry.png" width=500></td>
  </tr>
  <tr>
    <th>View Existing Entries</th>
    <th>Results</th>
  </tr>
  <tr>
    <td><img src="assets/view_entries.png" width=500></td>
    <td><img src="assets/results.png" width=500></td>
  </tr>
</table>

<br>

<h2 id="installation">2. Installation</h2>

```
git clone https://github.com/marcusvanwinden/work_log_csv.git
cd work_log_csv
python3 app.py
```
