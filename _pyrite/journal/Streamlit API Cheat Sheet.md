---
id: Streamlit API Cheet Sheet
---

# Import convention
>>> import streamlit as st
Pre-release features
Python
pip uninstall streamlit
pip install streamlit-nightly --upgrade
Learn more about experimental features

Command line
Python
streamlit cache clear
streamlit config show
streamlit docs
streamlit hello
streamlit help
streamlit init
streamlit run streamlit_app.py
streamlit version
Magic commands
Python
# Magic commands implicitly
# call st.write().
"_This_ is some **Markdown**"
my_variable
"dataframe:", my_data_frame
Display text
Python
st.write("Most objects") # df, err, func, keras!
st.write(["st", "is <", 3])
st.write_stream(my_generator)
st.write_stream(my_llm_stream)

st.text("Fixed width text")
st.markdown("_Markdown_")
st.latex(r""" e^{i\pi} + 1 = 0 """)
st.title("My title")
st.header("My header")
st.subheader("My sub")
st.code("for i in range(8): foo()")
st.badge("New")
st.html("<p>Hi!</p>")
Display data
Python
st.dataframe(my_dataframe)
st.table(data.iloc[0:10])
st.json({"foo":"bar","fu":"ba"})
st.metric("My metric", 42, 2)
Display media
Python
st.image("./header.png")
st.logo("logo.jpg")
st.pdf("my_document.pdf")
st.audio(data)
st.video(data)
st.video(data, subtitles="./subs.vtt")
Display charts
Python
st.area_chart(df)
st.bar_chart(df)
st.bar_chart(df, horizontal=True)
st.line_chart(df)
st.map(df)
st.scatter_chart(df)

st.altair_chart(chart)
st.graphviz_chart(fig)
st.plotly_chart(fig)
st.pydeck_chart(chart)
st.pyplot(fig)
st.vega_lite_chart(df, spec)

# Work with user selections
event = st.plotly_chart(
    df,
    on_select="rerun"
)
event = st.altair_chart(
    chart,
    on_select="rerun"
)
event = st.vega_lite_chart(
    df,
    spec,
    on_select="rerun"
)
To use Bokeh, see our custom component streamlit-bokeh.

Add elements to sidebar
Python
# Just add it after st.sidebar:
a = st.sidebar.radio("Select one:", [1, 2])

# Or use "with" notation:
with st.sidebar:
    st.radio("Select one:", [1, 2])
Columns
Python
# Two equal columns:
col1, col2 = st.columns(2)
col1.write("This is column 1")
col2.write("This is column 2")

# Three different columns:
col1, col2, col3 = st.columns([3, 1, 1])
# col1 is larger.

# Bottom-aligned columns
col1, col2 = st.columns(2, vertical_alignment="bottom")

# You can also use "with" notation:
with col1:
    st.radio("Select one:", [1, 2])
Tabs
Python
# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
    st.radio("Select one:", [1, 2])
Expandable containers
Python
expand = st.expander("My label", icon=":material/info:")
expand.write("Inside the expander.")
pop = st.popover("Button label")
pop.checkbox("Show all")

# You can also use "with" notation:
with expand:
    st.radio("Select one:", [1, 2])
Control flow
Python
# Stop execution immediately:
st.stop()
# Rerun script immediately:
st.rerun()
# Navigate to another page:
st.switch_page("pages/my_page.py")

# Define a navigation widget in your entrypoint file
pg = st.navigation(
    st.Page("page1.py", title="Home", url_path="home", default=True)
    st.Page("page2.py", title="Preferences", url_path="settings")
)
pg.run()

# Group multiple widgets:
with st.form(key="my_form"):
    username = st.text_input("Username")
    password = st.text_input("Password")
    st.form_submit_button("Login")

# Define a dialog function
@st.dialog("Welcome!")
def modal_dialog():
    st.write("Hello")

modal_dialog()

# Define a fragment
@st.fragment
def fragment_function():
    df = get_data()
    st.line_chart(df)
    st.button("Update")

fragment_function()
Display interactive widgets
Python
st.button("Click me")
st.download_button("Download file", data)
st.link_button("Go to gallery", url)
st.page_link("app.py", label="Home")
st.data_editor("Edit data", data)
st.checkbox("I agree")
st.feedback("thumbs")
st.pills("Tags", ["Sports", "Politics"])
st.radio("Pick one", ["cats", "dogs"])
st.segmented_control("Filter", ["Open", "Closed"])
st.toggle("Enable")
st.selectbox("Pick one", ["cats", "dogs"])
st.multiselect("Buy", ["milk", "apples", "potatoes"])
st.slider("Pick a number", 0, 100)
st.select_slider("Pick a size", ["S", "M", "L"])
st.text_input("First name")
st.number_input("Pick a number", 0, 10)
st.text_area("Text to translate")
st.date_input("Your birthday")
st.datetime_input("Event date and time")
st.time_input("Meeting time")
st.file_uploader("Upload a CSV")
st.audio_input("Record a voice message")
st.camera_input("Take a picture")
st.color_picker("Pick a color")

# Use widgets' returned values in variables:
for i in range(int(st.number_input("Num:"))):
    foo()
if st.sidebar.selectbox("I:",["f"]) == "f":
    b()
my_slider_val = st.slider("Quinn Mallory", 1, 88)
st.write(slider_val)

# Disable widgets to remove interactivity:
st.slider("Pick a number", 0, 100, disabled=True)
Build chat-based apps
Python
# Insert a chat message container.
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))

# Display a chat input widget at the bottom of the app.
st.chat_input("Say something")

# Display a chat input widget inline.
with st.container():
    st.chat_input("Say something")
Learn how to Build a basic LLM chat app

Mutate data
Python
# Add rows to a dataframe after
# showing it.
element = st.dataframe(df1)
element.add_rows(df2)

# Add rows to a chart after
# showing it.
element = st.line_chart(df1)
element.add_rows(df2)
Display code
Python
with st.echo():
    st.write("Code will be executed and printed")
Placeholders, help, and options
Python
# Replace any single element.
element = st.empty()
element.line_chart(...)
element.text_input(...)  # Replaces previous.

# Insert out of order.
elements = st.container()
elements.line_chart(...)
st.write("Hello")
elements.text_input(...)  # Appears above "Hello".

# Horizontal flex
flex = st.container(horizontal=True)
flex.button("A")
flex.button("B")

# Spacing
st.space("small")

st.help(pandas.DataFrame)
st.get_option(key)
st.set_option(key, value)
st.set_page_config(layout="wide")
st.query_params[key]
st.query_params.from_dict(params_dict)
st.query_params.get_all(key)
st.query_params.clear()
st.html("<p>Hi!</p>")
Connect to data sources
Python
st.connection("pets_db", type="sql")
conn = st.connection("sql")
conn = st.connection("snowflake")

class MyConnection(BaseConnection[myconn.MyConnection]):
    def _connect(self, **kwargs) -> MyConnection:
        return myconn.connect(**self._secrets, **kwargs)
    def query(self, query):
        return self._instance.query(query)
Optimize performance
Cache data objects
Python
# E.g. Dataframe computation, storing downloaded data, etc.
@st.cache_data
def foo(bar):
    # Do something expensive and return data
    return data
# Executes foo
d1 = foo(ref1)
# Does not execute foo
# Returns cached item by value, d1 == d2
d2 = foo(ref1)
# Different arg, so function foo executes
d3 = foo(ref2)
# Clear the cached value for foo(ref1)
foo.clear(ref1)
# Clear all cached entries for this function
foo.clear()
# Clear values from *all* in-memory or on-disk cached functions
st.cache_data.clear()
Cache global resources
Python
# E.g. TensorFlow session, database connection, etc.
@st.cache_resource
def foo(bar):
    # Create and return a non-data object
    return session
# Executes foo
s1 = foo(ref1)
# Does not execute foo
# Returns cached item by reference, s1 == s2
s2 = foo(ref1)
# Different arg, so function foo executes
s3 = foo(ref2)
# Clear the cached value for foo(ref1)
foo.clear(ref1)
# Clear all cached entries for this function
foo.clear()
# Clear all global resources from cache
st.cache_resource.clear()
Display progress and status
Python
# Show a spinner during a process
with st.spinner(text="In progress"):
    time.sleep(3)
    st.success("Done")

# Show and update progress bar
bar = st.progress(50)
time.sleep(3)
bar.progress(100)

with st.status("Authenticating...") as s:
    time.sleep(2)
    st.write("Some long response.")
    s.update(label="Response")

st.balloons()
st.snow()
st.toast("Warming up...")
st.error("Error message")
st.warning("Warning message")
st.info("Info message")
st.success("Success message")
st.exception(e)
Personalize apps for users
Python
# Authenticate users
if not st.user.is_logged_in:
    st.login("my_provider")
f"Hi, {st.user.name}"
st.logout()

# Get dictionaries of cookies, headers, locale, and browser data
st.context.cookies
st.context.headers
st.context.ip_address
st.context.is_embedded
st.context.locale
st.context.theme.type
st.context.timezone
st.context.timezone_offset
st.context.url
arrow_back
Previous: Quick reference
arrow_forward
Next: Release notes
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI





search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Develop/
API reference
API reference
Streamlit makes it easy for you to visualize, mutate, and share data. The API reference is organized by activity type, like displaying data or optimizing performance. Each section includes methods associated with the activity type, including examples.

Browse our API below and click to learn more about any of our available commands! 🎈

Display almost anything
Write and magic

st.write
Write arguments to the app.

st.write("Hello **world**!")
st.write(my_data_frame)
st.write(my_mpl_figure)
st.write_stream
Write generators or streams to the app with a typewriter effect.

st.write_stream(my_generator)
st.write_stream(my_llm_stream)
Magic
Any time Streamlit sees either a variable or literal value on its own line, it automatically writes that to your app using st.write

"Hello **world**!"
my_data_frame
my_mpl_figure
Text elements

screenshot
Markdown
Display string formatted as Markdown.

st.markdown("Hello **world**!")
screenshot
Title
Display text in title formatting.

st.title("The app title")
screenshot
Header
Display text in header formatting.

st.header("This is a header")
screenshot
Subheader
Display text in subheader formatting.

st.subheader("This is a subheader")
screenshot
Badge
Display a small, colored badge.

st.badge("New")
screenshot
Caption
Display text in small font.

st.caption("This is written small caption text")
screenshot
Code block
Display a code block with optional syntax highlighting.

st.code("a = 1234")
screenshot
Echo
Display some code in the app, then execute it. Useful for tutorials.

with st.echo():
  st.write('This code will be printed')
screenshot
LaTeX
Display mathematical expressions formatted as LaTeX.

st.latex("\int a x^2 \,dx")
screenshot
Preformatted text
Write fixed-width and preformatted text.

st.text("Hello world")
screenshot
Divider
Display a horizontal rule.

st.divider()
Get help
Display object’s doc string, nicely formatted.

st.help(st.write)
st.help(pd.DataFrame)
Render HTML
Renders HTML strings to your app.

st.html("<p>Foo bar.</p>")
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!


arrow_backward

arrow_forward













Data elements

screenshot
Dataframes
Display a dataframe as an interactive table.

st.dataframe(my_data_frame)
screenshot
Data editor
Display a data editor widget.

edited = st.data_editor(df, num_rows="dynamic")
screenshot
Column configuration
Configure the display and editing behavior of dataframes and data editors.

st.column_config.NumberColumn("Price (in USD)", min_value=0, format="$%d")
screenshot
Static tables
Display a static table.

st.table(my_data_frame)
screenshot
Metrics
Display a metric in big bold font, with an optional indicator of how the metric changed.

st.metric("My metric", 42, 2)
screenshot
Dicts and JSON
Display object or string as a pretty-printed JSON string.

st.json(my_dict)
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!


arrow_backward

arrow_forward















Chart elements

screenshot
Simple area charts
Display an area chart.

st.area_chart(my_data_frame)
screenshot
Simple bar charts
Display a bar chart.

st.bar_chart(my_data_frame)
screenshot
Simple line charts
Display a line chart.

st.line_chart(my_data_frame)
screenshot
Simple scatter charts
Display a line chart.

st.scatter_chart(my_data_frame)
screenshot
Scatterplots on maps
Display a map with points on it.

st.map(my_data_frame)
screenshot
Matplotlib
Display a matplotlib.pyplot figure.

st.pyplot(my_mpl_figure)
screenshot
Altair
Display a chart using the Altair library.

st.altair_chart(my_altair_chart)
screenshot
Vega-Lite
Display a chart using the Vega-Lite library.

st.vega_lite_chart(my_vega_lite_chart)
screenshot
Plotly
Display an interactive Plotly chart.

st.plotly_chart(my_plotly_chart)
screenshot
Bokeh
Display an interactive Bokeh chart.

st.bokeh_chart(my_bokeh_chart)
screenshot
PyDeck
Display a chart using the PyDeck library.

st.pydeck_chart(my_pydeck_chart)
screenshot
GraphViz
Display a graph using the dagre-d3 library.

st.graphviz_chart(my_graphviz_spec)
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!


arrow_backward

arrow_forward





















Input widgets

screenshot
Button
Display a button widget.

clicked = st.button("Click me")
screenshot
Download button
Display a download button widget.

st.download_button("Download file", file)
screenshot
Form button
Display a form submit button. For use with st.form.

st.form_submit_button("Sign up")
screenshot
Link button
Display a link button.

st.link_button("Go to gallery", url)
screenshot
Page link
Display a link to another page in a multipage app.

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="My profile")
screenshot
Checkbox
Display a checkbox widget.

selected = st.checkbox("I agree")
screenshot
Color picker
Display a color picker widget.

color = st.color_picker("Pick a color")
screenshot
Feedback
Display a rating or sentiment button group.

st.feedback("stars")
screenshot
Multiselect
Display a multiselect widget. The multiselect widget starts as empty.

choices = st.multiselect("Buy", ["milk", "apples", "potatoes"])
screenshot
Pills
Display a pill-button selection widget.

st.pills("Tags", ["Sports", "AI", "Politics"])
screenshot
Radio
Display a radio button widget.

choice = st.radio("Pick one", ["cats", "dogs"])
screenshot
Segmented control
Display a segmented-button selection widget.

st.segmented_control("Filter", ["Open", "Closed", "All"])
screenshot
Selectbox
Display a select widget.

choice = st.selectbox("Pick one", ["cats", "dogs"])
screenshot
Select-slider
Display a slider widget to select items from a list.

size = st.select_slider("Pick a size", ["S", "M", "L"])
screenshot
Toggle
Display a toggle widget.

activated = st.toggle("Activate")
screenshot
Number input
Display a numeric input widget.

choice = st.number_input("Pick a number", 0, 10)
screenshot
Slider
Display a slider widget.

number = st.slider("Pick a number", 0, 100)
screenshot
Date input
Display a date input widget.

date = st.date_input("Your birthday")
screenshot
Datetime input
Display a datetime input widget.

datetime = st.datetime_input("Schedule your event")
screenshot
Time input
Display a time input widget.

time = st.time_input("Meeting time")
screenshot
Chat input
Display a chat input widget.

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
screenshot
Text-area
Display a multi-line text input widget.

text = st.text_area("Text to translate")
screenshot
Text input
Display a single-line text input widget.

name = st.text_input("First name")
screenshot
Audio input
Display a widget that allows users to record with their microphone.

speech = st.audio_input("Record a voice message")
screenshot
Data editor
Display a data editor widget.

edited = st.data_editor(df, num_rows="dynamic")
screenshot
File uploader
Display a file uploader widget.

data = st.file_uploader("Upload a CSV")
screenshot
Camera input
Display a widget that allows users to upload images directly from a camera.

image = st.camera_input("Take a picture")
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!


arrow_backward

arrow_forward





















Media elements

screenshot
Image
Display an image or list of images.

st.image(numpy_array)
st.image(image_bytes)
st.image(file)
st.image("https://example.com/myimage.jpg")
screenshot
Logo
Display a logo in the upper-left corner of your app and its sidebar.

st.logo("logo.jpg")
screenshot
PDF
Display a PDF file.

st.pdf("my_document.pdf")
screenshot
Audio
Display an audio player.

st.audio(numpy_array)
st.audio(audio_bytes)
st.audio(file)
st.audio("https://example.com/myaudio.mp3", format="audio/mp3")
screenshot
Video
Display a video player.

st.video(numpy_array)
st.video(video_bytes)
st.video(file)
st.video("https://example.com/myvideo.mp4", format="video/mp4")
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!


arrow_backward

arrow_forward















Layouts and containers

screenshot
Columns
Insert containers laid out as side-by-side columns.

col1, col2 = st.columns(2)
col1.write("this is column 1")
col2.write("this is column 2")
screenshot
Container
Insert a multi-element container.

c = st.container()
st.write("This will show last")
c.write("This will show first")
c.write("This will show second")
screenshot
Modal dialog
Insert a modal dialog that can rerun independently from the rest of the script.

@st.dialog("Sign up")
def email_form():
    name = st.text_input("Name")
    email = st.text_input("Email")
screenshot
Empty
Insert a single-element container.

c = st.empty()
st.write("This will show last")
c.write("This will be replaced")
c.write("This will show first")
screenshot
Expander
Insert a multi-element container that can be expanded/collapsed.

with st.expander("Open to see more"):
  st.write("This is more content")
screenshot
Popover
Insert a multi-element popover container that can be opened/closed.

with st.popover("Settings"):
  st.checkbox("Show completed")
screenshot
Sidebar
Display items in a sidebar.

st.sidebar.write("This lives in the sidebar")
st.sidebar.button("Click me!")
screenshot
Space
Add vertical or horizontal space.

st.space("small")
screenshot
Tabs
Insert containers separated into tabs.

tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!




Chat elements

Streamlit provides a few commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.

st.chat_message lets you insert a chat message container into the app so you can display messages from the user or the app. Chat containers can contain other Streamlit elements, including charts, tables, text, and more. st.chat_input lets you display a chat input widget so the user can type in a message.

screenshot
Chat input
Display a chat input widget.

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
screenshot
Chat message
Insert a chat message container.

import numpy as np
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))
screenshot
Status container
Display output of long-running tasks in a container.

with st.status('Running'):
  do_something_slow()
st.write_stream
Write generators or streams to the app with a typewriter effect.

st.write_stream(my_generator)
st.write_stream(my_llm_stream)
Status elements

screenshot
Progress bar
Display a progress bar.

for i in range(101):
  st.progress(i)
  do_something_slow()
screenshot
Spinner
Temporarily displays a message while executing a block of code.

with st.spinner("Please wait..."):
  do_something_slow()
screenshot
Status container
Display output of long-running tasks in a container.

with st.status('Running'):
  do_something_slow()
screenshot
Toast
Briefly displays a toast message in the bottom-right corner.

st.toast('Butter!', icon='🧈')
screenshot
Balloons
Display celebratory balloons!

do_something()

# Celebrate when all done!
st.balloons()
screenshot
Snowflakes
Display celebratory snowflakes!

do_something()

# Celebrate when all done!
st.snow()
screenshot
Success box
Display a success message.

st.success("Match found!")
screenshot
Info box
Display an informational message.

st.info("Dataset is updated every day at midnight.")
screenshot
Warning box
Display warning message.

st.warning("Unable to fetch image. Skipping...")
screenshot
Error box
Display error message.

st.error("We encountered an error")
screenshot
Exception output
Display an exception.

e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!




App logic and configuration
Authentication and user info

Log in a user
st.login() starts an authentication flow with an identity provider.

st.login()
Log out a user
st.logout() removes a user's identity information.

st.logout()
User info
st.user returns information about a logged-in user.

if st.user.is_logged_in:
  st.write(f"Welcome back, {st.user.name}!")
Navigation and pages

screenshot
Navigation
Configure the available pages in a multipage app.

st.navigation({
    "Your account" : [log_out, settings],
    "Reports" : [overview, usage],
    "Tools" : [search]
})
screenshot
Page
Define a page in a multipage app.

home = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:"
)
screenshot
Page link
Display a link to another page in a multipage app.

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="My profile")
Switch page
Programmatically navigates to a specified page.

st.switch_page("pages/my_page.py")
Execution flow

screenshot
Modal dialog
Insert a modal dialog that can rerun independently from the rest of the script.

@st.dialog("Sign up")
def email_form():
    name = st.text_input("Name")
    email = st.text_input("Email")
Forms
Create a form that batches elements together with a “Submit" button.

with st.form(key='my_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    st.form_submit_button("Sign up")
Fragments
Define a fragment to rerun independently from the rest of the script.

@st.fragment(run_every="10s")
def fragment():
    df = get_data()
    st.line_chart(df)
Rerun script
Rerun the script immediately.

st.rerun()
Stop execution
Stops execution immediately.

st.stop()
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!




Caching and state

Cache data
Function decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).

@st.cache_data
def long_function(param1, param2):
  # Perform expensive computation here or
  # fetch data from the web here
  return data
Cache resource
Function decorator to cache functions that return global resources (e.g. database connections, ML models).

@st.cache_resource
def init_model():
  # Return a global resource here
  return pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
  )
Session state
Session state is a way to share variables between reruns, for each user session.

st.session_state['key'] = value
Query parameters
Get, set, or clear the query parameters that are shown in the browser's URL bar.

st.query_params[key] = value
st.query_params.clear()
Context
st.context provides a read-only interface to access cookies, headers, locale, and other browser-session information.

st.context.cookies
st.context.headers
Connections and databases
Setup your connection
screenshot
Create a connection
Connect to a data source or API

conn = st.connection('pets_db', type='sql')
pet_owners = conn.query('select * from pet_owners')
st.dataframe(pet_owners)
Built-in connections
screenshot
SnowflakeConnection
A connection to Snowflake.

conn = st.connection('snowflake')
screenshot
SQLConnection
A connection to a SQL database using SQLAlchemy.

conn = st.connection('sql')
Build your own connections
Connection base class
Build your own connection with BaseConnection.

class MyConnection(BaseConnection[myconn.MyConnection]):
    def _connect(self, **kwargs) -> MyConnection:
        return myconn.connect(**self._secrets, **kwargs)
    def query(self, query):
        return self._instance.query(query)
Secrets management
Secrets singleton
Access secrets from a local TOML file.

key = st.secrets["OpenAI_key"]
Secrets file
Save your secrets in a per-project or per-profile TOML file.

OpenAI_key = "<YOUR_SECRET_KEY>"
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!




Custom Components

V2 custom components
Register
Register a custom component.

my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
Mount
Mount a custom component.

my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
npm support code
Support code published through npm.

npm i @streamlit/component-v2-lib
Component
Type alias for the component function.

import { Component } from "@streamlit/component-v2-lib";
ComponentArgs
Type alias for the component arguments.

import { ComponentArgs } from "@streamlit/component-v2-lib";
ComponentState
Type alias for the component state.

import { ComponentState } from "@streamlit/component-v2-lib";
OptionalComponentCleanupFunction
Type alias for the component cleanup function.

import { OptionalComponentCleanupFunction } from "@streamlit/component-v2-lib";
V1 custom components
Declare a component
Create and register a custom component.

from st.components.v1 import declare_component
declare_component(
    "custom_slider",
    "/frontend",
)
HTML
Display an HTML string in an iframe.

from st.components.v1 import html
html(
    "<p>Foo bar.</p>"
)
iframe
Load a remote URL in an iframe.

from st.components.v1 import iframe
iframe(
    "docs.streamlit.io"
)
Configuration

Configuration file
Configures the default settings for your app.

your-project/
├── .streamlit/
│   └── config.toml
└── your_app.py
Get config option
Retrieve a single configuration option.

st.get_option("theme.primaryColor")
Set config option
Set a single configuration option. (This is very limited.)

st.set_option("deprecation.showPyplotGlobalUse", False)
Set page title, favicon, and more
Configures the default settings of the page.

st.set_page_config(
  page_title="My app",
  page_icon=":shark:",
)
Developer tools
App testing

st.testing.v1.AppTest
st.testing.v1.AppTest simulates a running Streamlit app for testing.

from streamlit.testing.v1 import AppTest

at = AppTest.from_file("streamlit_app.py")
at.secrets["WORD"] = "Foobar"
at.run()
assert not at.exception

at.text_input("word").input("Bazbat").run()
assert at.warning[0].value == "Try again."
AppTest.from_file
st.testing.v1.AppTest.from_file initializes a simulated app from a file.

from streamlit.testing.v1 import AppTest

at = AppTest.from_file("streamlit_app.py")
at.run()
AppTest.from_string
st.testing.v1.AppTest.from_string initializes a simulated app from a string.

from streamlit.testing.v1 import AppTest

at = AppTest.from_string(app_script_as_string)
at.run()
AppTest.from_function
st.testing.v1.AppTest.from_function initializes a simulated app from a function.

from streamlit.testing.v1 import AppTest

at = AppTest.from_function(app_script_as_callable)
at.run()
Block
A representation of container elements, including:

st.chat_message
st.columns
st.sidebar
st.tabs
The main body of the app.
# at.sidebar returns a Block
at.sidebar.button[0].click().run()
assert not at.exception
Element
The base class for representation of all elements, including:

st.title
st.header
st.markdown
st.dataframe
# at.title returns a sequence of Title
# Title inherits from Element
assert at.title[0].value == "My awesome app"
Button
A representation of st.button and st.form_submit_button.

at.button[0].click().run()
ChatInput
A representation of st.chat_input.

at.chat_input[0].set_value("What is Streamlit?").run()
Checkbox
A representation of st.checkbox.

at.checkbox[0].check().run()
ColorPicker
A representation of st.color_picker.

at.color_picker[0].pick("#FF4B4B").run()
DateInput
A representation of st.date_input.

release_date = datetime.date(2023, 10, 26)
at.date_input[0].set_value(release_date).run()
Multiselect
A representation of st.multiselect.

at.multiselect[0].select("New York").run()
NumberInput
A representation of st.number_input.

at.number_input[0].increment().run()
Radio
A representation of st.radio.

at.radio[0].set_value("New York").run()
SelectSlider
A representation of st.select_slider.

at.select_slider[0].set_range("A","C").run()
Selectbox
A representation of st.selectbox.

at.selectbox[0].select("New York").run()
Slider
A representation of st.slider.

at.slider[0].set_range(2,5).run()
TextArea
A representation of st.text_area.

at.text_area[0].input("Streamlit is awesome!").run()
TextInput
A representation of st.text_input.

at.text_input[0].input("Streamlit").run()
TimeInput
A representation of st.time_input.

at.time_input[0].increment().run()
Toggle
A representation of st.toggle.

at.toggle[0].set_value("True").run()
Third-party components


These are featured components created by our lovely community. For more examples and inspiration, check out our Components Gallery and Streamlit Extras!



---



search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started
Get started with Streamlit
This Get Started guide explains how Streamlit works, how to install Streamlit on your preferred operating system, and how to create your first Streamlit app!

downloading
Installation helps you set up your development environment. Walk through installing Streamlit on Windows, macOS, or Linux. Alternatively, code right in your browser with GitHub Codespaces or Streamlit in Snowflake.

description
Fundamentals introduces you to Streamlit's data model and development flow. You'll learn what makes Streamlit the most powerful way to build data apps, including the ability to display and style data, draw charts and maps, add interactive widgets, customize app layouts, cache computation, and define themes.

auto_awesome
First steps walks you through creating apps using core features to fetch and cache data, draw charts, plot information on a map, and use interactive widgets to filter results.

rocket_launch
Use GitHub Codespaces if you want to skip past local installation and code right in your browser. This guide uses Streamlit Community Cloud to help you automatically configure a codespace.

30 Days of Streamlit 🎈
30 Days of Streamlit 🎈 is a free, self-paced 30 day challenge that teaches you how to build and deploy data apps with Streamlit. Complete the daily challenges, share your solutions with us on Twitter and LinkedIn, and stop by the forum with any questions!

Start the challenge

arrow_forward
Next: Installation
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI




search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Installation
Install Streamlit
There are multiple ways to set up your development environment and install Streamlit. Developing locally with Python installed on your own computer is the most common scenario.

star
Tip
Try a Streamlit Playground that runs in your browser — no installation required. (Note that this is not how Streamlit is meant to be used, because it has many downsides. That's why it's a playground!)

arrow_forward
Instructions for the playground
Summary for experienced Python developers
To set up your Python environment and test your installation, execute the following terminal commands:

Terminal
pip install streamlit
streamlit hello

Copy
Jump to our Basic concepts.

Install Streamlit on your machine
Option 1: I like the command line
Install Streamlit on your own machine using tools like venv and pip.

arrow_forward
Instructions for the command line
Option 2: I prefer a graphical interface
Install Streamlit using the Anaconda Distribution graphical user interface. This is also the best approach if you're on Windows or don't have Python set up.

arrow_forward
Instructions for Anaconda Distribution
Create an app in the cloud
Option 1: I want a free cloud environment
Use Streamlit Community Cloud with GitHub Codespaces so you don't have to go through the trouble of installing Python and setting up an environment.

arrow_forward
Instructions for GitHub Codespaces
Option 2: I need something secure, controlled, and in the cloud
Use Streamlit in Snowflake to code your apps in the cloud, right alongside your data with role-based access controls.

arrow_forward
Instructions for Snowflake
arrow_back
Previous: Get started
arrow_forward
Next: Use Streamlit Playground
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
Install Streamlit - Streamlit Docs






search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Fundamentals/
Basic concepts
Basic concepts of Streamlit
Working with Streamlit is simple. First you sprinkle a few Streamlit commands into a normal Python script, then you run it with streamlit run:

Terminal
streamlit run your_script.py [-- script args]

Copy
As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab in your default web browser. The app is your canvas, where you'll draw charts, text, widgets, tables, and more.

What gets drawn in the app is up to you. For example st.text writes raw text to your app, and st.line_chart draws — you guessed it — a line chart. Refer to our API documentation to see all commands that are available to you.

push_pin
Note
When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself.

Another way of running Streamlit is to run it as a Python module. This can be useful when configuring an IDE like PyCharm to work with Streamlit:

Terminal
# Running
python -m streamlit run your_script.py

# is equivalent to:
streamlit run your_script.py

Copy
star
Tip
You can also pass a URL to streamlit run! This is great when combined with GitHub Gists. For example:

Terminal
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py

Copy
Development flow
Every time you want to update your app, save the source file. When you do that, Streamlit detects if there is a change and asks you whether you want to rerun your app. Choose "Always rerun" at the top-right of your screen to automatically update your app every time you change its source code.

This allows you to work in a fast interactive loop: you type some code, save it, try it out live, then type some more code, save it, try it out, and so on until you're happy with the results. This tight loop between coding and viewing results live is one of the ways Streamlit makes your life easier.

star
Tip
While developing a Streamlit app, it's recommended to lay out your editor and browser windows side by side, so the code and the app can be seen at the same time. Give it a try!

As of Streamlit version 1.10.0 and higher, Streamlit apps cannot be run from the root directory of Linux distributions. If you try to run a Streamlit app from the root directory, Streamlit will throw a FileNotFoundError: [Errno 2] No such file or directory error. For more information, see GitHub issue #5239.

If you are using Streamlit version 1.10.0 or higher, your main script should live in a directory other than the root directory. When using Docker, you can use the WORKDIR command to specify the directory where your main script lives. For an example of how to do this, read Create a Dockerfile.

Data flow
Streamlit's architecture allows you to write apps the same way you write plain Python scripts. To unlock this, Streamlit apps have a unique data flow: any time something must be updated on the screen, Streamlit reruns your entire Python script from top to bottom.

This can happen in two situations:

Whenever you modify your app's source code.

Whenever a user interacts with widgets in the app. For example, when dragging a slider, entering text in an input box, or clicking a button.

Whenever a callback is passed to a widget via the on_change (or on_click) parameter, the callback will always run before the rest of your script. For details on the Callbacks API, please refer to our Session State API Reference Guide.

And to make all of this fast and seamless, Streamlit does some heavy lifting for you behind the scenes. A big player in this story is the @st.cache_data decorator, which allows developers to skip certain costly computations when their apps rerun. We'll cover caching later in this page.

Display and style data
There are a few ways to display data (tables, arrays, data frames) in Streamlit apps. Below, you will be introduced to magic and st.write(), which can be used to write anything from text to tables. After that, let's take a look at methods designed specifically for visualizing data.

Use magic
You can also write to your app without calling any Streamlit methods. Streamlit supports "magic commands," which means you don't have to use st.write() at all! To see this in action try this snippet:

Python

Try it
arrow_outward
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

Copy
Any time that Streamlit sees a variable or a literal value on its own line, it automatically writes that to your app using st.write(). For more information, refer to the documentation on magic commands.

Write a data frame
Along with magic commands, st.write() is Streamlit's "Swiss Army knife". You can pass almost anything to st.write(): text, data, Matplotlib figures, Altair charts, and more. Don't worry, Streamlit will figure it out and render things the right way.

Python
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

Copy
There are other data specific functions like st.dataframe() and st.table() that you can also use for displaying data. Let's understand when to use these features and how to add colors and styling to your data frames.

You might be asking yourself, "why wouldn't I always use st.write()?" There are a few reasons:

Magic and st.write() inspect the type of data that you've passed in, and then decide how to best render it in the app. Sometimes you want to draw it another way. For example, instead of drawing a dataframe as an interactive table, you may want to draw it as a static table by using st.table(df).
The second reason is that other methods return an object that can be used and modified, either by adding data to it or replacing it.
Finally, if you use a more specific Streamlit method you can pass additional arguments to customize its behavior.
For example, let's create a data frame and change its formatting with a Pandas Styler object. In this example, you'll use Numpy to generate a random sample, and the st.dataframe() method to draw an interactive table.

push_pin
Note
This example uses Numpy to generate a random sample, but you can use Pandas DataFrames, Numpy arrays, or plain Python arrays.

Python
import streamlit as st
import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

Copy
Let's expand on the first example using the Pandas Styler object to highlight some elements in the interactive table.

Python
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

Copy
Streamlit also has a method for static table generation: st.table().

Python
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

Copy
Draw charts and maps
Streamlit supports several popular data charting libraries like Matplotlib, Altair, deck.gl, and more. In this section, you'll add a bar chart, line chart, and a map to your app.

Draw a line chart
You can easily add a line chart to your app with st.line_chart(). We'll generate a random sample using Numpy and then chart it.

Python
import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

Copy
Plot a map
With st.map() you can display data points on a map. Let's use Numpy to generate some sample data and plot it on a map of San Francisco.

Python
import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

Copy
Widgets
When you've got the data or model into the state that you want to explore, you can add in widgets like st.slider(), st.button() or st.selectbox(). It's really straightforward — treat widgets as variables:

Python
import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

Copy
On first run, the app above should output the text "0 squared is 0". Then every time a user interacts with a widget, Streamlit simply reruns your script from top to bottom, assigning the current state of the widget to your variable in the process.

For example, if the user moves the slider to position 10, Streamlit will rerun the code above and set x to 10 accordingly. So now you should see the text "10 squared is 100".

Widgets can also be accessed by key, if you choose to specify a string to use as the unique key for the widget:

Python
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

Copy
Every widget with a key is automatically added to Session State. For more information about Session State, its association with widget state, and its limitations, see Session State API Reference Guide.

Use checkboxes to show/hide data
One use case for checkboxes is to hide or show a specific chart or section in an app. st.checkbox() takes a single argument, which is the widget label. In this sample, the checkbox is used to toggle a conditional statement.

Python
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

Copy
Use a selectbox for options
Use st.selectbox to choose from a series. You can write in the options you want, or pass through an array or data frame column.

Let's use the df data frame we created earlier.

Python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

Copy
Layout
Streamlit makes it easy to organize your widgets in a left panel sidebar with st.sidebar. Each element that's passed to st.sidebar is pinned to the left, allowing users to focus on the content in your app while still having access to UI controls.

For example, if you want to add a selectbox and a slider to a sidebar, use st.sidebar.slider and st.sidebar.selectbox instead of st.slider and st.selectbox:

Python
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

Copy
Beyond the sidebar, Streamlit offers several other ways to control the layout of your app. st.columns lets you place widgets side-by-side, and st.expander lets you conserve space by hiding away large content.

Python
import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

Copy
push_pin
Note
st.echo and st.spinner are not currently supported inside the sidebar or layout options. Rest assured, though, we're currently working on adding support for those too!

Show progress
When adding long running computations to an app, you can use st.progress() to display status in real time.

First, let's import time. We're going to use the time.sleep() method to simulate a long running computation:

Python
import time

Copy
Now, let's create a progress bar:

Python
import streamlit as st
import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'

Copy
arrow_back
Previous: Fundamentals
arrow_forward
Next: Advanced concepts
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
Basic concepts of Streamlit - Streamlit Docs






search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Fundamentals/
Advanced concepts
Advanced concepts of Streamlit
Now that you know how a Streamlit app runs and handles data, let's talk about being efficient. Caching allows you to save the output of a function so you can skip over it on rerun. Session State lets you save information for each user that is preserved between reruns. This not only allows you to avoid unecessary recalculation, but also allows you to create dynamic pages and handle progressive processes.

Caching
Caching allows your app to stay performant even when loading data from the web, manipulating large datasets, or performing expensive computations.

The basic idea behind caching is to store the results of expensive function calls and return the cached result when the same inputs occur again. This avoids repeated execution of a function with the same input values.

To cache a function in Streamlit, you need to apply a caching decorator to it. You have two choices:

st.cache_data is the recommended way to cache computations that return data. Use st.cache_data when you use a function that returns a serializable data object (e.g. str, int, float, DataFrame, dict, list). It creates a new copy of the data at each function call, making it safe against mutations and race conditions. The behavior of st.cache_data is what you want in most cases – so if you're unsure, start with st.cache_data and see if it works!
st.cache_resource is the recommended way to cache global resources like ML models or database connections. Use st.cache_resource when your function returns unserializable objects that you don’t want to load multiple times. It returns the cached object itself, which is shared across all reruns and sessions without copying or duplication. If you mutate an object that is cached using st.cache_resource, that mutation will exist across all reruns and sessions.
Example:

Python
@st.cache_data
def long_running_function(param1, param2):
    return …

Copy
In the above example, long_running_function is decorated with @st.cache_data. As a result, Streamlit notes the following:

The name of the function ("long_running_function").
The value of the inputs (param1, param2).
The code within the function.
Before running the code within long_running_function, Streamlit checks its cache for a previously saved result. If it finds a cached result for the given function and input values, it will return that cached result and not rerun function's code. Otherwise, Streamlit executes the function, saves the result in its cache, and proceeds with the script run. During development, the cache updates automatically as the function code changes, ensuring that the latest changes are reflected in the cache.

Streamlit's two caching decorators and their use cases. Use st.cache_data for anything you'd store in a database. Use st.cache_resource for anything you can't store in a database, like a connection to a database or a machine learning model.
Streamlit's two caching decorators and their use cases.

For more information about the Streamlit caching decorators, their configuration parameters, and their limitations, see Caching.

Session State
Session State provides a dictionary-like interface where you can save information that is preserved between script reruns. Use st.session_state with key or attribute notation to store and recall values. For example, st.session_state["my_key"] or st.session_state.my_key. Remember that widgets handle their statefulness all by themselves, so you won't always need to use Session State!

What is a session?
A session is a single instance of viewing an app. If you view an app from two different tabs in your browser, each tab will have its own session. So each viewer of an app will have a Session State tied to their specific view. Streamlit maintains this session as the user interacts with the app. If the user refreshes their browser page or reloads the URL to the app, their Session State resets and they begin again with a new session.

Examples of using Session State
Here's a simple app that counts the number of times the page has been run. Every time you click the button, the script will rerun.

Python
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")

Copy
First run: The first time the app runs for each user, Session State is empty. Therefore, a key-value pair is created ("counter":0). As the script continues, the counter is immediately incremented ("counter":1) and the result is displayed: "This page has run 1 times." When the page has fully rendered, the script has finished and the Streamlit server waits for the user to do something. When that user clicks the button, a rerun begins.

Second run: Since "counter" is already a key in Session State, it is not reinitialized. As the script continues, the counter is incremented ("counter":2) and the result is displayed: "This page has run 2 times."

There are a few common scenarios where Session State is helpful. As demonstrated above, Session State is used when you have a progressive process that you want to build upon from one rerun to the next. Session State can also be used to prevent recalculation, similar to caching. However, the differences are important:

Caching associates stored values to specific functions and inputs. Cached values are accessible to all users across all sessions.
Session State associates stored values to keys (strings). Values in session state are only available in the single session where it was saved.
If you have random number generation in your app, you'd likely use Session State. Here's an example where data is generated randomly at the beginning of each session. By saving this random information in Session State, each user gets different random data when they open the app but it won't keep changing on them as they interact with it. If you select different colors with the picker you'll see that the data does not get re-randomized with each rerun. (If you open the app in a new tab to start a new session, you'll see different data!)

Python
import streamlit as st
import pandas as pd
import numpy as np

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)

Copy
If you are pulling the same data for all users, you'd likely cache a function that retrieves that data. On the other hand, if you pull data specific to a user, such as querying their personal information, you may want to save that in Session State. That way, the queried data is only available in that one session.

As mentioned in Basic concepts, Session State is also related to widgets. Widgets are magical and handle statefulness quietly on their own. As an advanced feature however, you can manipulate the value of widgets within your code by assigning keys to them. Any key assigned to a widget becomes a key in Session State tied to the value of the widget. This can be used to manipulate the widget. After you finish understanding the basics of Streamlit, check out our guide on Widget behavior to dig in the details if you're interested.

Connections
As hinted above, you can use @st.cache_resource to cache connections. This is the most general solution which allows you to use almost any connection from any Python library. However, Streamlit also offers a convenient way to handle some of the most popular connections, like SQL! st.connection takes care of the caching for you so you can enjoy fewer lines of code. Getting data from your database can be as easy as:

Python
import streamlit as st

conn = st.connection("my_database")
df = conn.query("select * from my_table")
st.dataframe(df)

Copy
Of course, you may be wondering where your username and password go. Streamlit has a convenient mechanism for Secrets management. For now, let's just see how st.connection works very nicely with secrets. In your local project directory, you can save a .streamlit/secrets.toml file. You save your secrets in the toml file and st.connection just uses them! For example, if you have an app file streamlit_app.py your project directory may look like this:

your-LOCAL-repository/
├── .streamlit/
│   └── secrets.toml # Make sure to gitignore this!
└── streamlit_app.py
For the above SQL example, your secrets.toml file might look like the following:

TOML
[connections.my_database]
    type="sql"
    dialect="mysql"
    username="xxx"
    password="xxx"
    host="example.com" # IP or URL
    port=3306 # Port number
    database="mydb" # Database name

Copy
Since you don't want to commit your secrets.toml file to your repository, you'll need to learn how your host handles secrets when you're ready to publish your app. Each host platform may have a different way for you to pass your secrets. If you use Streamlit Community Cloud for example, each deployed app has a settings menu where you can load your secrets. After you've written an app and are ready to deploy, you can read all about how to Deploy your app on Community Cloud.

arrow_back
Previous: Basic concepts
arrow_forward
Next: Additional features
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
Advanced concepts of Streamlit - Streamlit Docs





search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Fundamentals/
Additional features
Additional Streamlit features
So you've read all about Streamlit's Basic concepts and gotten a taste of caching and Session State in Advanced concepts. But what about the bells and whistles? Here's a quick look at some extra features to take your app to the next level.

Theming
Streamlit supports Light and Dark themes out of the box. Streamlit will first check if the user viewing an app has a Light or Dark mode preference set by their operating system and browser. If so, then that preference will be used. Otherwise, the Light theme is applied by default.

You can also change the active theme from "⋮" → "Settings".

Changing Themes
Want to add your own theme to an app? The "Settings" menu has a theme editor accessible by clicking on "Edit active theme". You can use this editor to try out different colors and see your app update live.

Editing Themes
When you're happy with your work, themes can be saved by setting config options in the [theme] config section. After you've defined a theme for your app, it will appear as "Custom Theme" in the theme selector and will be applied by default instead of the included Light and Dark themes.

More information about the options available when defining a theme can be found in the theme option documentation.

push_pin
Note
The theme editor menu is available only in local development. If you've deployed your app using Streamlit Community Cloud, the "Edit active theme" button will no longer be displayed in the "Settings" menu.

star
Tip
Another way to experiment with different theme colors is to turn on the "Run on save" option, edit your config.toml file, and watch as your app reruns with the new theme colors applied.

Pages
As apps grow large, it becomes useful to organize them into multiple pages. This makes the app easier to manage as a developer and easier to navigate as a user. Streamlit provides a powerful way to create multipage apps using st.Page and st.navigation. Just create your pages and connect them with navigation as follows:

Create an entry point script that defines and connects your pages
Create separate Python files for each page's content
Use st.Page to define your pages and st.navigation to connect them
Here's an example of a three-page app:

streamlit_app.py
Python
import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()

Copy
main_page.py
Python
import streamlit as st

# Main page content
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

Copy
page_2.py
Python
import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

Copy
page_3.py
Python
import streamlit as st

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")

Copy

Now run streamlit run streamlit_app.py and view your shiny new multipage app! The navigation menu will automatically appear, allowing users to switch between pages.


Our documentation on Multipage apps teaches you how to add pages to your app, including how to define pages, structure and run multipage apps, and navigate between pages. Once you understand the basics, create your first multipage app!

Custom components
If you can't find the right component within the Streamlit library, try out custom components to extend Streamlit's built-in functionality. Explore and browse through popular, community-created components in the Components gallery. If you dabble in frontend development, you can build your own custom component with Streamlit's components API.

Static file serving
As you learned in Streamlit fundamentals, Streamlit runs a server that clients connect to. That means viewers of your app don't have direct access to the files which are local to your app. Most of the time, this doesn't matter because Streamlt commands handle that for you. When you use st.image(<path-to-image>) your Streamlit server will access the file and handle the necessary hosting so your app viewers can see it. However, if you want a direct URL to an image or file you'll need to host it. This requires setting the correct configuration and placing your hosted files in a directory named static. For example, your project could look like:

Terminal
your-project/
├── static/
│   └── my_hosted-image.png
└── streamlit_app.py

Copy
To learn more, read our guide on Static file serving.

App testing
Good development hygiene includes testing your code. Automated testing allows you to write higher quality code, faster! Streamlit has a built-in testing framework that let's you build tests easily. Use your favorite testing framework to run your tests. We like pytest. When you test a Streamlit app, you simulate running the app, declare user input, and inspect the results. You can use GitHub workflows to automate your tests and get instant alerts about breaking changes. Learn more in our guide to App testing.

arrow_back
Previous: Advanced concepts
arrow_forward
Next: Summary
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
Additional Streamlit features - Streamlit Docs




search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Fundamentals/
Summary
App model summary
Now that you know a little more about all the individual pieces, let's close the loop and review how it works together:

Streamlit apps are Python scripts that run from top to bottom.
Every time a user opens a browser tab pointing to your app, the script is executed and a new session starts.
As the script executes, Streamlit draws its output live in a browser.
Every time a user interacts with a widget, your script is re-executed and Streamlit redraws its output in the browser.
The output value of that widget matches the new value during that rerun.
Scripts use the Streamlit cache to avoid recomputing expensive functions, so updates happen very fast.
Session State lets you save information that persists between reruns when you need more than a simple widget.
Streamlit apps can contain multiple pages, which are defined in separate .py files in a pages folder.
The Streamlit app model
arrow_back
Previous: Additional features
arrow_forward
Next: First steps
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
App model summary - Streamlit Docs



search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
Fundamentals/
Basic concepts
Basic concepts of Streamlit
Working with Streamlit is simple. First you sprinkle a few Streamlit commands into a normal Python script, then you run it with streamlit run:

Terminal
streamlit run your_script.py [-- script args]

Copy
As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab in your default web browser. The app is your canvas, where you'll draw charts, text, widgets, tables, and more.

What gets drawn in the app is up to you. For example st.text writes raw text to your app, and st.line_chart draws — you guessed it — a line chart. Refer to our API documentation to see all commands that are available to you.

push_pin
Note
When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself.

Another way of running Streamlit is to run it as a Python module. This can be useful when configuring an IDE like PyCharm to work with Streamlit:

Terminal
# Running
python -m streamlit run your_script.py

# is equivalent to:
streamlit run your_script.py

Copy
star
Tip
You can also pass a URL to streamlit run! This is great when combined with GitHub Gists. For example:

Terminal
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py

Copy
Development flow
Every time you want to update your app, save the source file. When you do that, Streamlit detects if there is a change and asks you whether you want to rerun your app. Choose "Always rerun" at the top-right of your screen to automatically update your app every time you change its source code.

This allows you to work in a fast interactive loop: you type some code, save it, try it out live, then type some more code, save it, try it out, and so on until you're happy with the results. This tight loop between coding and viewing results live is one of the ways Streamlit makes your life easier.

star
Tip
While developing a Streamlit app, it's recommended to lay out your editor and browser windows side by side, so the code and the app can be seen at the same time. Give it a try!

As of Streamlit version 1.10.0 and higher, Streamlit apps cannot be run from the root directory of Linux distributions. If you try to run a Streamlit app from the root directory, Streamlit will throw a FileNotFoundError: [Errno 2] No such file or directory error. For more information, see GitHub issue #5239.

If you are using Streamlit version 1.10.0 or higher, your main script should live in a directory other than the root directory. When using Docker, you can use the WORKDIR command to specify the directory where your main script lives. For an example of how to do this, read Create a Dockerfile.

Data flow
Streamlit's architecture allows you to write apps the same way you write plain Python scripts. To unlock this, Streamlit apps have a unique data flow: any time something must be updated on the screen, Streamlit reruns your entire Python script from top to bottom.

This can happen in two situations:

Whenever you modify your app's source code.

Whenever a user interacts with widgets in the app. For example, when dragging a slider, entering text in an input box, or clicking a button.

Whenever a callback is passed to a widget via the on_change (or on_click) parameter, the callback will always run before the rest of your script. For details on the Callbacks API, please refer to our Session State API Reference Guide.

And to make all of this fast and seamless, Streamlit does some heavy lifting for you behind the scenes. A big player in this story is the @st.cache_data decorator, which allows developers to skip certain costly computations when their apps rerun. We'll cover caching later in this page.

Display and style data
There are a few ways to display data (tables, arrays, data frames) in Streamlit apps. Below, you will be introduced to magic and st.write(), which can be used to write anything from text to tables. After that, let's take a look at methods designed specifically for visualizing data.

Use magic
You can also write to your app without calling any Streamlit methods. Streamlit supports "magic commands," which means you don't have to use st.write() at all! To see this in action try this snippet:

Python

Try it
arrow_outward
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

Copy
Any time that Streamlit sees a variable or a literal value on its own line, it automatically writes that to your app using st.write(). For more information, refer to the documentation on magic commands.

Write a data frame
Along with magic commands, st.write() is Streamlit's "Swiss Army knife". You can pass almost anything to st.write(): text, data, Matplotlib figures, Altair charts, and more. Don't worry, Streamlit will figure it out and render things the right way.

Python
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

Copy
There are other data specific functions like st.dataframe() and st.table() that you can also use for displaying data. Let's understand when to use these features and how to add colors and styling to your data frames.

You might be asking yourself, "why wouldn't I always use st.write()?" There are a few reasons:

Magic and st.write() inspect the type of data that you've passed in, and then decide how to best render it in the app. Sometimes you want to draw it another way. For example, instead of drawing a dataframe as an interactive table, you may want to draw it as a static table by using st.table(df).
The second reason is that other methods return an object that can be used and modified, either by adding data to it or replacing it.
Finally, if you use a more specific Streamlit method you can pass additional arguments to customize its behavior.
For example, let's create a data frame and change its formatting with a Pandas Styler object. In this example, you'll use Numpy to generate a random sample, and the st.dataframe() method to draw an interactive table.

push_pin
Note
This example uses Numpy to generate a random sample, but you can use Pandas DataFrames, Numpy arrays, or plain Python arrays.

Python
import streamlit as st
import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

Copy
Let's expand on the first example using the Pandas Styler object to highlight some elements in the interactive table.

Python
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

Copy
Streamlit also has a method for static table generation: st.table().

Python
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

Copy
Draw charts and maps
Streamlit supports several popular data charting libraries like Matplotlib, Altair, deck.gl, and more. In this section, you'll add a bar chart, line chart, and a map to your app.

Draw a line chart
You can easily add a line chart to your app with st.line_chart(). We'll generate a random sample using Numpy and then chart it.

Python
import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

Copy
Plot a map
With st.map() you can display data points on a map. Let's use Numpy to generate some sample data and plot it on a map of San Francisco.

Python
import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

Copy
Widgets
When you've got the data or model into the state that you want to explore, you can add in widgets like st.slider(), st.button() or st.selectbox(). It's really straightforward — treat widgets as variables:

Python
import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

Copy
On first run, the app above should output the text "0 squared is 0". Then every time a user interacts with a widget, Streamlit simply reruns your script from top to bottom, assigning the current state of the widget to your variable in the process.

For example, if the user moves the slider to position 10, Streamlit will rerun the code above and set x to 10 accordingly. So now you should see the text "10 squared is 100".

Widgets can also be accessed by key, if you choose to specify a string to use as the unique key for the widget:

Python
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

Copy
Every widget with a key is automatically added to Session State. For more information about Session State, its association with widget state, and its limitations, see Session State API Reference Guide.

Use checkboxes to show/hide data
One use case for checkboxes is to hide or show a specific chart or section in an app. st.checkbox() takes a single argument, which is the widget label. In this sample, the checkbox is used to toggle a conditional statement.

Python
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

Copy
Use a selectbox for options
Use st.selectbox to choose from a series. You can write in the options you want, or pass through an array or data frame column.

Let's use the df data frame we created earlier.

Python
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

Copy
Layout
Streamlit makes it easy to organize your widgets in a left panel sidebar with st.sidebar. Each element that's passed to st.sidebar is pinned to the left, allowing users to focus on the content in your app while still having access to UI controls.

For example, if you want to add a selectbox and a slider to a sidebar, use st.sidebar.slider and st.sidebar.selectbox instead of st.slider and st.selectbox:

Python
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

Copy
Beyond the sidebar, Streamlit offers several other ways to control the layout of your app. st.columns lets you place widgets side-by-side, and st.expander lets you conserve space by hiding away large content.

Python
import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

Copy
push_pin
Note
st.echo and st.spinner are not currently supported inside the sidebar or layout options. Rest assured, though, we're currently working on adding support for those too!

Show progress
When adding long running computations to an app, you can use st.progress() to display status in real time.

First, let's import time. We're going to use the time.sleep() method to simulate a long running computation:

Python
import time

Copy
Now, let's create a progress bar:

Python
import streamlit as st
import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'

Copy
arrow_back
Previous: Fundamentals
arrow_forward
Next: Advanced concepts
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie settings

forum
Ask AI
Basic concepts of Streamlit - Streamlit Docs



search
Search

rocket_launch
Get started

Installation
add
Fundamentals
add
First steps
remove
Create an app
Create a multipage app
code
Develop

Concepts
add
API reference
add
Tutorials
add
Quick reference
add
web_asset
Deploy

Concepts
add
Streamlit Community Cloud
add
Snowflake
Other platforms
add
school
Knowledge base

FAQ
Installing dependencies
Deployment issues
Home/
Get started/
First steps/
Create an app
Create an app
If you've made it this far, chances are you've installed Streamlit and run through the basics in Basic concepts and Advanced concepts. If not, now is a good time to take a look.

The easiest way to learn how to use Streamlit is to try things out yourself. As you read through this guide, test each method. As long as your app is running, every time you add a new element to your script and save, Streamlit's UI will ask if you'd like to rerun the app and view the changes. This allows you to work in a fast interactive loop: you write some code, save it, review the output, write some more, and so on, until you're happy with the results. The goal is to use Streamlit to create an interactive app for your data or model and along the way to use Streamlit to review, debug, perfect, and share your code.

In this guide, you're going to use Streamlit's core features to create an interactive app; exploring a public Uber dataset for pickups and drop-offs in New York City. When you're finished, you'll know how to fetch and cache data, draw charts, plot information on a map, and use interactive widgets, like a slider, to filter results.

star
Tip
If you'd like to skip ahead and see everything at once, the complete script is available below.

Create your first app
Streamlit is more than just a way to make data apps, it’s also a community of creators that share their apps and ideas and help each other make their work better. Please come join us on the community forum. We love to hear your questions, ideas, and help you work through your bugs — stop by today!

The first step is to create a new Python script. Let's call it uber_pickups.py.

Open uber_pickups.py in your favorite IDE or text editor, then add these lines:

Python
import streamlit as st
import pandas as pd
import numpy as np
Every good app has a title, so let's add one:

Python
st.title('Uber pickups in NYC')
Now it's time to run Streamlit from the command line:

Terminal
streamlit run uber_pickups.py
Running a Streamlit app is no different than any other Python script. Whenever you need to view the app, you can use this command.

star
Tip
Did you know you can also pass a URL to streamlit run? This is great when combined with GitHub Gists. For example:

Terminal
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
As usual, the app should automatically open in a new tab in your browser.

Fetch some data
Now that you have an app, the next thing you'll need to do is fetch the Uber dataset for pickups and drop-offs in New York City.

Let's start by writing a function to load the data. Add this code to your script:

Python
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
You'll notice that load_data is a plain old function that downloads some data, puts it in a Pandas dataframe, and converts the date column from text to datetime. The function accepts a single parameter (nrows), which specifies the number of rows that you want to load into the dataframe.

Now let's test the function and review the output. Below your function, add these lines:

Python
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
You'll see a few buttons in the upper-right corner of your app asking if you'd like to rerun the app. Choose Always rerun, and you'll see your changes automatically each time you save.

Ok, that's underwhelming...

It turns out that it takes a long time to download data, and load 10,000 lines into a dataframe. Converting the date column into datetime isn’t a quick job either. You don’t want to reload the data each time the app is updated – luckily Streamlit allows you to cache the data.

Effortless caching
Try adding @st.cache_data before the load_data declaration:

Python
@st.cache_data
def load_data(nrows):
Then save the script, and Streamlit will automatically rerun your app. Since this is the first time you’re running the script with @st.cache_data, you won't see anything change. Let’s tweak your file a little bit more so that you can see the power of caching.

Replace the line data_load_state.text('Loading data...done!') with this:

Python
data_load_state.text("Done! (using st.cache_data)")
Now save. See how the line you added appeared immediately? If you take a step back for a second, this is actually quite amazing. Something magical is happening behind the scenes, and it only takes one line of code to activate it.

How's it work?
Let's take a few minutes to discuss how @st.cache_data actually works.

When you mark a function with Streamlit’s cache annotation, it tells Streamlit that whenever the function is called that it should check two things:

The input parameters you used for the function call.
The code inside the function.
If this is the first time Streamlit has seen both these items, with these exact values, and in this exact combination, it runs the function and stores the result in a local cache. The next time the function is called, if the two values haven't changed, then Streamlit knows it can skip executing the function altogether. Instead, it reads the output from the local cache and passes it on to the caller -- like magic.

"But, wait a second," you’re saying to yourself, "this sounds too good to be true. What are the limitations of all this awesomesauce?"

Well, there are a few:

Streamlit will only check for changes within the current working directory. If you upgrade a Python library, Streamlit's cache will only notice this if that library is installed inside your working directory.
If your function is not deterministic (that is, its output depends on random numbers), or if it pulls data from an external time-varying source (for example, a live stock market ticker service) the cached value will be none-the-wiser.
Lastly, you should avoid mutating the output of a function cached with st.cache_data since cached values are stored by reference.
While these limitations are important to keep in mind, they tend not to be an issue a surprising amount of the time. Those times, this cache is really transformational.

star
Tip
Whenever you have a long-running computation in your code, consider refactoring it so you can use @st.cache_data, if possible. Please read Caching for more details.

Now that you know how caching with Streamlit works, let’s get back to the Uber pickup data.

Inspect the raw data
It's always a good idea to take a look at the raw data you're working with before you start working with it. Let's add a subheader and a printout of the raw data to the app:

Python
st.subheader('Raw data')
st.write(data)
In the Basic concepts guide you learned that st.write will render almost anything you pass to it. In this case, you're passing in a dataframe and it's rendering as an interactive table.

st.write tries to do the right thing based on the data type of the input. If it isn't doing what you expect you can use a specialized command like st.dataframe instead. For a full list, see API reference.

Draw a histogram
Now that you've had a chance to take a look at the dataset and observe what's available, let's take things a step further and draw a histogram to see what Uber's busiest hours are in New York City.

To start, let's add a subheader just below the raw data section:

Python
st.subheader('Number of pickups by hour')
Use NumPy to generate a histogram that breaks down pickup times binned by hour:

Python
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
Now, let's use Streamlit's st.bar_chart() method to draw this histogram.

Python
st.bar_chart(hist_values)
Save your script. This histogram should show up in your app right away. After a quick review, it looks like the busiest time is 17:00 (5 P.M.).

To draw this diagram we used Streamlit's native bar_chart() method, but it's important to know that Streamlit supports more complex charting libraries like Altair, Bokeh, Plotly, Matplotlib and more. For a full list, see supported charting libraries.

Plot data on a map
Using a histogram with Uber's dataset helped us determine what the busiest times are for pickups, but what if we wanted to figure out where pickups were concentrated throughout the city. While you could use a bar chart to show this data, it wouldn't be easy to interpret unless you were intimately familiar with latitudinal and longitudinal coordinates in the city. To show pickup concentration, let's use Streamlit st.map() function to overlay the data on a map of New York City.

Add a subheader for the section:

Python
st.subheader('Map of all pickups')
Use the st.map() function to plot the data:

Python
st.map(data)
Save your script. The map is fully interactive. Give it a try by panning or zooming in a bit.

After drawing your histogram, you determined that the busiest hour for Uber pickups was 17:00. Let's redraw the map to show the concentration of pickups at 17:00.

Locate the following code snippet:

Python
st.subheader('Map of all pickups')
st.map(data)
Replace it with:

Python
hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
You should see the data update instantly.

To draw this map we used the st.map function that's built into Streamlit, but if you'd like to visualize complex map data, we encourage you to take a look at the st.pydeck_chart.

Filter results with a slider
In the last section, when you drew the map, the time used to filter results was hardcoded into the script, but what if we wanted to let a reader dynamically filter the data in real time? Using Streamlit's widgets you can. Let's add a slider to the app with the st.slider() method.

Locate hour_to_filter and replace it with this code snippet:

Python
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
Use the slider and watch the map update in real time.

Use a button to toggle data
Sliders are just one way to dynamically change the composition of your app. Let's use the st.checkbox function to add a checkbox to your app. We'll use this checkbox to show/hide the raw data table at the top of your app.

Locate these lines:

Python
st.subheader('Raw data')
st.write(data)
Replace these lines with the following code:

Python
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
We're sure you've got your own ideas. When you're done with this tutorial, check out all the widgets that Streamlit exposes in our API Reference.

Let's put it all together
That's it, you've made it to the end. Here's the complete script for our interactive app.

star
Tip
If you've skipped ahead, after you've created your script, the command to run Streamlit is streamlit run [app name].

Python
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
Share your app
After you’ve built a Streamlit app, it's time to share it! To show it off to the world you can use Streamlit Community Cloud to deploy, manage, and share your app for free.

It works in 3 simple steps:

Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
Sign into share.streamlit.io
Click 'Deploy an app' and then paste in your GitHub URL
That's it! 🎈 You now have a publicly deployed app that you can share with the world. Click to learn more about how to use Streamlit Community Cloud.

Get help
That's it for getting started, now you can go and build your own apps! If you run into difficulties here are a few things you can do.

Check out our community forum and post a question
Quick help from command line with streamlit help
Go through our Knowledge Base for tips, step-by-step tutorials, and articles that answer your questions about creating and deploying Streamlit apps.
Read more documentation! Check out:
Concepts for things like caching, theming, and adding statefulness to apps.
API reference for examples of every Streamlit command.
arrow_back
Previous: First steps
arrow_forward
Next: Create a multipage app
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.

forum
Ask AI



---



search
Search

⌘K

dark_modelight_mode
rocket_launch
Get started

code
Develop

web_asset
Deploy

school
Knowledge base

Home/
Get started/
First steps/
Create a multipage app
Create a multipage app
In Additional features, we introduced multipage apps, including how to define pages, structure and run multipage apps, and navigate between pages in the user interface. You can read more details in our guide to Multipage apps

In this guide, let’s put our understanding of multipage apps to use by converting the previous version of our streamlit hello app to a multipage app!

Motivation
Before Streamlit 1.10.0, the streamlit hello command was a large single-page app. As there was no support for multiple pages, we resorted to splitting the app's content using st.selectbox in the sidebar to choose what content to run. The content is comprised of three demos for plotting, mapping, and dataframes.

Here's what the code and single-page app looked like:

hello.py (👈 Toggle to expand)

Built with Streamlit 🎈
Fullscreen
open_in_new
Notice how large the file is! Each app “page" is written as a function, and the selectbox is used to pick which page to display. As our app grows, maintaining the code requires a lot of additional overhead. Moreover, we’re limited by the st.selectbox UI to choose which “page" to run, we cannot customize individual page titles with st.set_page_config, and we’re unable to navigate between pages using URLs.

Convert an existing app into a multipage app
Now that we've identified the limitations of a single-page app, what can we do about it? Armed with our knowledge from the previous section, we can convert the existing app to be a multipage app, of course! At a high level, we need to perform the following steps:

Create a new pages folder in the same folder where the “entrypoint file" (hello.py) lives
Rename our entrypoint file to Hello.py , so that the title in the sidebar is capitalized
Create three new files inside of pages:
pages/1_📈_Plotting_Demo.py
pages/2_🌍_Mapping_Demo.py
pages/3_📊_DataFrame_Demo.py
Move the contents of the plotting_demo, mapping_demo, and data_frame_demo functions into their corresponding new files from Step 3
Run streamlit run Hello.py to view your newly converted multipage app!
Now, let’s walk through each step of the process and view the corresponding changes in code.

Create the entrypoint file
Hello.py
Python
import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

Copy

We rename our entrypoint file to Hello.py , so that the title in the sidebar is capitalized and only the code for the intro page is included. Additionally, we’re able to customize the page title and favicon — as it appears in the browser tab with st.set_page_config. We can do so for each of our pages too!


Notice how the sidebar does not contain page labels as we haven’t created any pages yet.

Create multiple pages
A few things to remember here:

We can change the ordering of pages in our MPA by adding numbers to the beginning of each Python file. If we add a 1 to the front of our file name, Streamlit will put that file first in the list.
The name of each Streamlit app is determined by the file name, so to change the app name you need to change the file name!
We can add some fun to our app by adding emojis to our file names that will render in our Streamlit app.
Each page will have its own URL, defined by the name of the file.
Check out how we do all this below! For each new page, we create a new file inside the pages folder, and add the appropriate demo code into it.


pages/1_📈_Plotting_Demo.py

pages/2_🌍_Mapping_Demo.py

pages/3_📊_DataFrame_Demo.py

With our additional pages created, we can now put it all together in the final step below.

Run the multipage app
To run your newly converted multipage app, run:

Terminal
streamlit run Hello.py

Copy
That’s it! The Hello.py script now corresponds to the main page of your app, and other scripts that Streamlit finds in the pages folder will also be present in the new page selector that appears in the sidebar.


Built with Streamlit 🎈
Fullscreen
open_in_new
Next steps
Congratulations! 🎉 If you've read this far, chances are you've learned to create both single-page and multipage apps. Where you go from here is entirely up to your creativity! We’re excited to see what you’ll build now that adding additional pages to your apps is easier than ever. Try adding more pages to the app we've just built as an exercise. Also, stop by the forum to show off your multipage apps with the Streamlit community! 🎈

Here are a few resources to help you get started:

Deploy your app for free on Streamlit's Community Cloud.
Post a question or share your multipage app on our community forum.
Check out our documentation on Multipage apps.
Read through Concepts for things like caching, theming, and adding statefulness to apps.
Browse our API reference for examples of every Streamlit command.
arrow_back
Previous: Create an app
arrow_forward
Next: Develop
forum
Still have questions?
Our forums are full of helpful information and Streamlit experts.

Home
Contact Us
Community
© 2026 Snowflake Inc.Cookie policy

forum
Ask AI



# Further Research:

https://docs.streamlit.io/develop/concepts

https://docs.streamlit.io/develop/api-reference

https://docs.streamlit.io/develop/tutorials

