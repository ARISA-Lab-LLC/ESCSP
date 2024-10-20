def escsp_get_psd(folder, plots_folder, filelist=None, eclipse_type = "Total", verbose=False):
    if verbose: print(folder)
    ESID=filename_2_ESID(folder)
    if verbose: print("ESID #=" + ESID)
    plot_1_name=os.path.join(plots_folder, "PSD_plot_"+ESID+".png")
    if verbose: print("plot_1_name= "+plot_1_name)
    plot_1a_name=os.path.join(plots_folder, "PSD_plot_"+ESID+".png")

    #Welch plots
    plot_2a_name=os.path.join(plots_folder, "PSD_Welch_plot_"+ESID+".png")
    if verbose: print("plot_2a_name (Welch)= "+plot_2a_name)
    plot_2b_name=os.path.join(plots_folder, "PSD_Bartlett_plot_"+ESID+".png")
    if verbose: print("plot_2b_name (Bartlett)= "+plot_2b_name)


    eclipse_data_csv=os.path.join(folder, "eclipse_data.csv")


    if os.path.isfile(eclipse_data_csv) :
        df=pd.read_csv(eclipse_data_csv, header=[0])
        time_format="%Y-%m-%d %H:%M:%S"
        if verbose: print("success! " + eclipse_data_csv) 
        if type(df["SecondContactTimeUTC"].values[0]) == type("test"):
        #if eclipse_type == "Annular" or eclipse_type == "Total":
#set the eclipse start time
            chars_to_remove=["\"", "\'", "[", "]"]
            second_contact=str(df["FirstContactDate"].values[0]+" "+df["SecondContactTimeUTC"].values[0])
            for char_to_remove in chars_to_remove:
                second_contact.replace(char_to_remove, '')
            print(second_contact)
        #eclipse_start_time = datetime.datetime(2023, 10, 14, 17, 34) 
            eclipse_start_time = datetime.datetime.strptime(second_contact, time_format) 
#set the eclipse end time
        #eclipse_end_time = datetime.datetime(2023, 10, 14, 17, 39)
            third_contact = str(df["FirstContactDate"].values[0]+" "+df["ThirdContactTimeUTC"].values[0])
            for char_to_remove in chars_to_remove:
                third_contact.replace(char_to_remove, '')
            eclipse_end_time =  datetime.datetime.strptime(third_contact, time_format) 
        else:
            max_eclipse=datetime.datetime.strptime(
                df["FirstContactDate"].values[0]+ " " + df["TotalEclipseTimeUTC"].values[0], time_format)
            eclipse_start_time=max_eclipse-datetime.timedelta(minutes=3)
            eclipse_end_time=max_eclipse+datetime.timedelta(minutes=3)

        two_days_before_start_time=eclipse_start_time-datetime.timedelta(hours=48)
        two_days_before_end_time=eclipse_end_time-datetime.timedelta(hours=48)

        one_day_before_start_time=eclipse_start_time-datetime.timedelta(hours=24)   
        one_day_before_end_time=eclipse_end_time-datetime.timedelta(hours=24)

#Get all of the recording files at the site
        recording_files=glob.glob(os.path.join(folder,"*."+"WAV"))
        if verbose: print(len(recording_files))   

        
        eclipse_files=None
        two_days_before_files=None
        one_day_before_files=None                      

        fs_ecl_wel=None
        fs_odb_wel=None
        fs_tdb_wel=None                     

        fs_ecl_bart=None
        fs_odb_bart=None
        fs_tdb_bart=None
        test_arr=np.ndarray(shape=(2,2), dtype=float, order='F')
        
        two_days_before_files=get_files_between_times(recording_files, two_days_before_start_time, two_days_before_end_time)     
        one_day_before_files=get_files_between_times(recording_files, one_day_before_start_time, one_day_before_end_time)
        eclipse_files=get_files_between_times(recording_files, eclipse_start_time, eclipse_end_time)


#IF the filelist parameter is set, then write the names of the files to the filelst file.  
        if filelist:
            if os.path.isfile(filelist):
                list_file=filelist
            else:
                list_file=os.path.join(folder, ESID+'_Analysis_Files.csv')
            
            if eclipse_files:
                df_=pd.DataFrame({'Eclipse Files': eclipse_files}) 
                if two_days_before_files:
                    df.insert(1, 'Two Days Before Files', two_days_before_files, True)
                else: df=pd.DataFrame({'Two Days Before Files': ["None"]}) 
                if one_day_before_files:
                    df.insert(1, 'One Day Before Files', one_day_before_files, True)
                else: df=pd.DataFrame({'One Day Before Files': ["None"]})       

            else: 
                df=pd.DataFrame({'Eclipse Files': ["None"]})    
            
            df.to_csv(list_file, index=False)

        if eclipse_files: 
            eclipse_wav, fs_ecl=combine_wave_files(eclipse_files, verbose=verbose)
            #f0, eclipse_psd=scipy.signal.periodogram(eclipse_wav, fs_ecl)
            fig, ax =plt.subplots()
            ax.psd(eclipse_wav, Fs=fs_ecl, color="orange", label="Eclipse Day")
            fs_ecl_wel, eclipse_wav_psd_welch=calc_psd(eclipse_wav, fs_ecl)
            fs_ecl_bart, eclipse_wav_psd_bart=calc_psd(eclipse_wav, fs_ecl, Bartlett=True)


            if two_days_before_files :
                print("Length of filelist: " + str(len(two_days_before_files)))
                two_days_before_wav, fs_tdb = combine_wave_files(two_days_before_files, verbose=verbose)
                #f2, two_days_before_psd=scipy.signal.periodogram(two_days_before_wav, fs_tdb)
                ax.psd(two_days_before_wav, Fs=fs_tdb, color="green", label="Two Days Before")
                fs_tdb_wel, tdb_wav_psd_welch=calc_psd(two_days_before_wav, fs_tdb)
                fs_tdb_bart, tdb_wav_psd_bart=calc_psd(two_days_before_wav, fs_tdb, Bartlett=True)

            if one_day_before_files: 
                one_day_before_wav, fs_odb = combine_wave_files(one_day_before_files, verbose=verbose)
                #f1, one_day_before_psd=scipy.signal.periodogram(one_day_before_wav, fs_odb)
                ax.psd(one_day_before_wav, Fs=fs_odb, color="blue", label="One Day Before")
                fs_odb_wel, odb_wav_psd_welch=calc_psd(one_day_before_wav, fs_odb)
                fs_odb_bart, odb_wav_psd_bart=calc_psd(one_day_before_wav, fs_odb, Bartlett=True)


                legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
                plt.savefig(plot_1_name)
                if verbose: print("Saved file "+plot_1_name)    
                plt.savefig(plot_1a_name)
                if verbose: print("Saved file "+plot_1a_name)
                plt.close(fig)

        #Make Plots of the Welch PSD

        
        if type(fs_ecl_wel) == type(test_arr):

            plt.figure()
            plt.title("PSD Welch's Method "+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            plt.semilogy(fs_ecl_wel, eclipse_wav_psd_welch,color="orange", label="Eclipse Day")
            
            if type(fs_odb_wel) == type(test_arr):
                 plt.semilogy(fs_odb_wel, odb_wav_psd_welch, color="blue", label="One Day Before")
            if type(fs_tdb_wel) == type(test_arr):
                 plt.semilogy(fs_tdb_wel, tdb_wav_psd_welch, color="green", label="Two Days Before")
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [V**2/Hz]')
            plt.legend(loc='upper center', shadow=True, fontsize='large')

            plt.savefig(plot_2a_name)
            if verbose: print("Saved file "+plot_2a_name)
            plt.close(fig)
            
        #Make Plots of the Bartlett PSD
        if type(fs_ecl_bart) == type(test_arr):

            plt.figure()
            plt.title("PSD Bartlett's Method "+ESID+" Eclipse on "+str(df["FirstContactDate"].values[0]))
            plt.semilogy(fs_ecl_bart, eclipse_wav_psd_bart,color="orange", label="Eclipse Day")
            if type(fs_odb_bart) == type(test_arr):

                 plt.semilogy(fs_odb_bart, odb_wav_psd_bart, color="blue", label="One Day Before")
            if type(fs_tdb_bart) == type(test_arr):
                 plt.semilogy(fs_tdb_bart, tdb_wav_psd_bart, color="green", label="Two Days Before")
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [V**2/Hz]')
            plt.legend(loc='upper center', shadow=True, fontsize='large')

            plt.savefig(plot_2b_name)
            if verbose: print("Saved file "+plot_2b_name)
            plt.close(fig)
            

    else:
        print("No file "+eclipse_data_csv+" found.")