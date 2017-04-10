using Newtonsoft.Json;
using System;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using Newtonsoft.Json.Linq;

namespace NLP_WPF
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        // globals
        static int counter = 0;
        static Articles artlist = null;
        static string[] indextracker = null;
        static int minlines = 0;
        static int minlinescounter = 0;
        static int[][] idtracker = null;
        static Summary sumobj = null;
        public MainWindow()
        {
            InitializeComponent();
            init();
        }

        public void init()
        {
            CastToJson("result.json");
            Updatecontent(0);
            idtracker = new int[artlist.articles.Count][];
            sumobj = new Summary();
            sumobj.summary = new System.Collections.Generic.List<SummaryObj>();
            
        }

        // Converting input Json to Object
        private void CastToJson(string filename)
        {
            artlist = new Articles();
            artlist.articles = new System.Collections.Generic.List<Article>();

            string jsontext = File.ReadAllText(filename, Encoding.UTF8);
            dynamic test = JsonConvert.DeserializeObject(jsontext);

            foreach (var obj in test)
            {
                Article art = new Article();
                art.url = obj.url;
                art.title = obj.title;
                art.content = new System.Collections.Generic.List<string>();

                foreach (var s in obj.content)
                    art.content.Add(s.ToString());

                artlist.articles.Add(art);
            }

            Updatecontent(0);
        }

        // Change the article content to selected category
        private void btn_update_Click_1(object sender, RoutedEventArgs e)
        {
            var selectedtag = ((System.Windows.FrameworkElement)cbox.SelectedValue).Tag.ToString();

            switch (selectedtag)
            {
                case "C":
                    //readJson("Sample.json");
                    CastToJson("cinema.json");
                    break;
                case "P":
                    CastToJson("statenews.json");
                    break;
                case "S":
                    CastToJson("sports.json");
                    break;
            }
            counter = 0;
        }

        // read json file from input file
        bool readJson(String filename)
        {
            try
            {
                string jsontext = File.ReadAllText(filename, Encoding.UTF8);

                if (jsontext.Length > 0)
                {
                    artlist = JsonConvert.DeserializeObject<Articles>(jsontext);

                    Updatecontent(0);
                }
                
                

            }
            catch(Exception exp)
            {

            }

            return true;
        }

        // Chnage the article as per selected index
        public void Updatecontent(int index)
        {
            

            if(index>= 0 && artlist!=null && artlist.articles!=null && artlist.articles.Count > 0 && artlist.articles.Count>index)
            {
                Article art = artlist.articles[index];

                grid_content.Children.Clear();

                url.Content ="URL : "+ art.url.ToString();
                title.Content ="Title : "+ art.title.ToString();

                for (int i = 0; i < art.content.Count; i++)
                {
                    CheckBox cb = new CheckBox();
                    cb.Name = "CB_"+i.ToString();
                    cb.Content = art.content[i];
                    cb.Margin = new System.Windows.Thickness { Left = 10, Top = (i+1)*20, Right = 0, Bottom = 0 };
                    cb.Checked += Cb_Checked;
                    cb.Unchecked += Cb_Unchecked;
                    grid_content.Children.Add(cb);
                }

                indextracker = new string[art.content.Count];

                int lines = art.content.Count;

                lines = Convert.ToInt16( lines * 0.2);

                if (lines < 4)
                    minlines = 4;
                else
                    minlines = lines;
                minlinescounter = 0;
                reset("Please select "+minlines+" lines");
            }
        }

        // Uncheck the checkbox- event handler
        private void Cb_Unchecked(object sender, RoutedEventArgs e)
        {
            CheckBox cb = sender as CheckBox;
            string name = cb.Name.ToString().Split('_')[1];

            int index = Convert.ToInt16(name);
            indextracker[index] = "";
            minlinescounter--;

            if (minlinescounter<=4)
                reset("Please select " + minlines + " lines. ");
        }

        // check the checkbox event handler
        private void Cb_Checked(object sender, RoutedEventArgs e)
        {
            CheckBox cb = sender as CheckBox;
            if (minlinescounter >= minlines)
            {
                reset("Cannot select more than " + minlines);
                return;
            }
            else
            {
                minlinescounter++;
                
            }
            
            string name = cb.Name.ToString().Split('_')[1];

            int index = Convert.ToInt16(name);

            indextracker[index] = cb.Content.ToString();
            
        }

        // generate the summary 
        private void btn_json_Click(object sender, RoutedEventArgs e)
        {
            if (sumobj != null)
            {
                string jsontext = JsonConvert.SerializeObject(sumobj);
                string filename = ((System.Windows.FrameworkElement)cbox.SelectedValue).Tag.ToString()+"_" + DateTime.Today.ToString("dd/mm/yyyy").Replace('/','_') + ".json";
                File.WriteAllText(filename, jsontext);
                reset(filename+" generated and saved successfully.");
            }
        }

        // fetch the next article
        private void btn_next_Click(object sender, RoutedEventArgs e)
        {
            if (artlist != null && artlist.articles != null && artlist.articles.Count > counter)
            {
                storeCurrentArticle();
                counter++;
                Updatecontent(counter);
            }
        }

        // fetch the previous article
        private void btn_previous_Click(object sender, RoutedEventArgs e)
        {
            if (artlist != null && artlist.articles != null && artlist.articles.Count > counter && counter > 0)
            {
                storeCurrentArticle();
                counter--;
                Updatecontent(counter);
            }
        }



        // store current article selection to global obj
        private void storeCurrentArticle()
        {
            if (indextracker != null)
            {
                SummaryObj obj = new SummaryObj();
                obj.ArticleNumber = counter;
                obj.LineNumbers = new System.Collections.Generic.List<int>();

                string summary = "";
                for (int i = 0; i < indextracker.Length; i++)
                {
                    if (indextracker[i] != null && indextracker[i].Length > 0)
                    {
                        summary += indextracker[i];
                        obj.LineNumbers.Add(i);
                    }
                }
                obj.text = summary;
                sumobj.summary.Add(obj);
            }
        }
        // update the status button
        public void reset(string message)
        {
            lb_status.Content = message;
        }
    }
}
