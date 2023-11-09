# @views.route("/edit-credit/<int:row_number>", methods=['GET', 'POST'])
# @login_required
# def edit_credit(row_number):
#     platform_names = get_platform_names()
#     existing_data = pd.read_csv(CREDIT_CSV)

#     if row_number < 0 or row_number >= len(existing_data):
#         flash("Invalid row number. The row does not exist.", category='error')
#         return redirect(url_for('views.home'))

#     row_data = existing_data.iloc[row_number]
#     row_data = row_data.fillna("")

#     if request.method == 'POST':

#         row_data['platform_name'] = request.form.get('platform_name')
#         row_data['owner'] = request.form.get('owner')
#         row_data['balance'] = request.form.get('balance')
#         row_data['cvv'] = request.form.get('cvv')
#         row_data['address'] = request.form.get('address')
#         row_data['card_holder'] = request.form.get('card_holder')
#         row_data['card_type'] = request.form.get('card_type')
#         row_data['card_website'] = request.form.get('card_website')
#         row_data['website_username'] = request.form.get('web_username')
#         row_data['website_password'] = request.form.get('web_password')
#         row_data['email'] = request.form.get('email')
#         row_data['email_password'] = request.form.get('email_password')
#         row_data['expiration_date'] = request.form.get('date_exp')
#         row_data['card_number'] = request.form.get('card_number')
#         row_data['document_reference'] = request.form.get('doc_reff')
#         row_data['notes'] = request.form.get('notes')

#         existing_data.iloc[row_number] = row_data
#         existing_data.to_csv(CREDIT_CSV, index=False)
#         flash('Credit edited!', category='success')
#         return redirect(url_for('views.home'))

#     return render_template('edit_credit.html', user=current_user, row_data=row_data, row_number=row_number, platform_names=platform_names)




# @views.route("/edit-service/<int:row_number>", methods=['GET', 'POST'])
# @login_required
# def edit_service(row_number):
#     platform_names = get_platform_names()
#     existing_data = pd.read_csv(SERVICE_CSV)

#     if row_number < 0 or row_number >= len(existing_data):
#         flash("Invalid row number. The row does not exist.", category='error')
#         return redirect(url_for('views.home'))

#     row_data = existing_data.iloc[row_number]
#     row_data = row_data.fillna("")

#     if request.method == 'POST':

#         row_data['platform_name'] = request.form.get('platform_name')
#         row_data['used_by'] = request.form.get('used_by')
#         row_data['service_type'] = request.form.get('service_type')
#         row_data['website'] = request.form.get('website')
#         row_data['web_username'] = request.form.get('web_username')
#         row_data['web_password'] = request.form.get('web_password')
#         row_data['email'] = request.form.get('email')
#         row_data['email_password'] = request.form.get('email_password')
#         row_data['ip'] = request.form.get('ip')
#         row_data['ip_username'] = request.form.get('ip_username')
#         row_data['ip_password'] = request.form.get('ip_password')
#         row_data['date_exp'] = request.form.get('user-date')
#         row_data['doc_reff'] = request.form.get('doc_reff')
#         row_data['phone'] = request.form.get('phone')
#         row_data['country'] = request.form.get('country')
#         row_data['etc'] = request.form.get('etc')

#         existing_data.iloc[row_number] = row_data
#         existing_data.to_csv(SERVICE_CSV, index=False)
#         flash('Service edited!', category='success')
#         return redirect(url_for('views.home'))

#     return render_template('edit_service.html', user=current_user, row_data=row_data, row_number=row_number, platform_names=platform_names)


    # Check if the CSV file exists, and create it if it doesn't
    # if not os.path.isfile(PLATFORM_CSV):
    #     # Create an empty DataFrame with the appropriate columns
    #     initial_data = pd.DataFrame(columns=['platform_name', 'date_created'])
    #     # Save it as the CSV file
    #     initial_data.to_csv(PLATFORM_CSV, index=False)

    # platform_names = get_platform_names()

    # if request.method == 'POST':
    #     platform_name = request.form.get('platform_name')
    #     date_created = date.today()

    #     if len(platform_name) < 1:
    #         flash('Platform name cannot be null!', category='error')
    #     elif platform_name in platform_names:
    #         flash('The platform already exists.', category='error')
    #     else:
    #         new_platform = pd.DataFrame({
    #             'platform_name': [platform_name],
    #             'date_created': [date_created],
    #         })

    #         try:
    #             existing_data = pd.read_csv(PLATFORM_CSV)

    #             if 'platform_name' in existing_data.columns:
    #                 # Check for duplicate platform names
    #                 if platform_name in existing_data['platform_name'].values:
    #                     flash('The platform already exists.', category='error')
    #                     return render_template('create_platform.html', user=current_user)
    #         except FileNotFoundError:
    #             existing_data = pd.DataFrame(columns=new_platform.columns)

    #         new_data = pd.concat([existing_data, new_platform], ignore_index=True)
    #         new_data.to_csv(PLATFORM_CSV, index=False)
    #         flash('Platform created!', category='success')
    #         return redirect(url_for('views.home'))

    # return render_template('create_platform.html', user=current_user)



# @views.route("/create-platform-user", methods=['GET', 'POST'])
# @login_required
# def create_platform_user():
#     platform_names = get_platform_names()

#     if request.method == 'POST':
#         # Get form data
#         name = request.form.get('name')
#         birth_date = request.form.get('birth_date')
#         phone = request.form.get('phone')
#         address = request.form.get('address')
#         facebook_username = request.form.get('facebook_username')
#         facebook_password = request.form.get('facebook_password')
#         linkedIn_username = request.form.get('linkedIn_username')
#         linkedIn_password = request.form.get('linkedIn_password')
#         payoneer_username = request.form.get('payoneer_username')
#         payoneer_password = request.form.get('payoneer_password')
#         paypal_username = request.form.get('paypal_username')
#         paypal_password = request.form.get('paypal_password')
#         instagram_username = request.form.get('instagram_username')
#         instagram_password = request.form.get('instagram_password')
#         tiktok_username = request.form.get('tiktok_username')
#         tiktok_password = request.form.get('tiktok_password')
#         email1 = request.form.get('email1')
#         email_password1 = request.form.get('email_password1')
#         email2 = request.form.get('email2')
#         email_password2 = request.form.get('email_password2')
#         wp_username = request.form.get('wp_username')
#         wp_password = request.form.get('wp_password')
#         wp_site = request.form.get('wp_site')
#         hosting_website = request.form.get('hosting_website')
#         hosting_username = request.form.get('hosting_username')
#         hosting_password = request.form.get('hosting_password')
#         document_reference = request.form.get('document_reference')
#         notes = request.form.get('notes')
#         platform_name = request.form.get('platform_name')
#         country = request.form.get('country')
#         owner = request.form.get('owner')
#         date_created = date.today()
#         id = str(uuid.uuid4())

#         # Create a new row as a dictionary
#         new_agent = pd.DataFrame({
#             'id': [id],
#             'name': [name],
#             'birth_date': [birth_date],
#             'phone': [phone],
#             'address': [address],
#             'facebook_username': [facebook_username],
#             'facebook_password': [facebook_password],
#             'linkedIn_username': [linkedIn_username],
#             'linkedIn_password': [linkedIn_password],
#             'payoneer_username': [payoneer_username],
#             'payoneer_password': [payoneer_password],
#             'paypal_username': [paypal_username],
#             'paypal_password': [paypal_password],
#             'instagram_username': [instagram_username],
#             'instagram_password': [instagram_password],
#             'tiktok_username': [tiktok_username],
#             'tiktok_password': [tiktok_password],
#             'email1': [email1],
#             'email_password1': [email_password1],
#             'email2': [email2],
#             'email_password2': [email_password2],
#             'wp_username': [wp_username],
#             'wp_password': [wp_password],
#             'wp_site': [wp_site],
#             'document_reference': [document_reference],
#             'hosting_website': [hosting_website],
#             'hosting_username': [hosting_username],
#             'hosting_password': [hosting_password],
#             'notes': [notes],
#             'platform_name': [platform_name],
#             'country': [country],
#             'owner': [owner],
#             'date_created': [date_created],
#         })

#         try:
#             existing_data = pd.read_csv(AGENTE_CSV)
#         except FileNotFoundError:
#             existing_data = pd.DataFrame(columns=new_agent.columns)

#         new_data = pd.concat([existing_data, new_agent], ignore_index=True)
#         new_data.to_csv(AGENTE_CSV, index=False)
#         flash('Agent created!', category='success')
#         return redirect(url_for('views.create_platform_user'))

#     return render_template('create_platform_user.html', user=current_user, platform_names=platform_names)
