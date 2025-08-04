from django.urls import path

from accountapp.views import *

urlpatterns = [
    path('register_driver/', RegisterDriver, name='register_driver'),
    path('driver-activate/<uidb64>/<token>/', DriverActivation , name='driver_activate'),
    path('driver-login/', DriverLogin , name='driver_login'),
    path('gmail-data/', JsonGmailDataAPI , name='gmail_data'),
    path('news-data/', JsonNewsDataAPI , name='news_data'),
    path('news-data-list/', JsonNewsDataListAPI , name='news_data_list'),
    path('cnbc-news-data-list/', JsonCNBCNewsDataListAPI , name='cnbc_news_data_list'),
    path('apple-news-data-list/', JsonAPPLENewsDataListAPI , name='apple_news_data_list'),
    path('roku-news-data-list/', JsonROKUNewsDataListAPI , name='roku_news_data_list'),
    path('tesla-news-data-list/', JsonTeslaNewsDataListAPI, name='tesla_news_data_list'),
    path('c3ai-news-data-list/', JsonC3AiNewsDataListAPI, name='c3ai_news_data_list'),
    path('rivian-news-data-list/', JsonRivianNewsDataListAPI, name='rivian_news_data_list'),
    
    path('json-yahoo-api/', JsonYahooAPI, name='json_yahoo_api'),
    path('json-yahoo-hist-api/', JsonYahooHistAPI, name='json_yahoo_hist-api'),
    path('json-yahoo-dynamic-api/', JsonYahooDynamicAPI),
    path('json-yahoo-finance-info-api/', JsonYahooFinanceInfoAPI),

    path('json-array-merge/', JsonArrayMergeDataAPI),
    
    path('query-json-file/', QueryJsonfileDataAPI),
    path('query-json-file/<str:user_hashkey>/', QueryJsonfileDataAPIHashkey),
    
    # path('model-json-query/', ModelJsonQueryDataAPI),
    path('model-json-query-new/', ModelJsonQueryDataNewAPI),
    path('model-json-query-new/<str:user_hashkey>/', ModelJsonQueryDataNewAPIHashkey),
    
    path('process-log/', ProcessLogAPI),
    path('internal-process-log/', InternalProcessLogAPI),
    path('heartbeat/', HeartbeatAPI),
    path('process-restart/', ProcessRestartAPI),
    
    path('normal-log/', NormalLogAPI),

    
    path('logger/', LoggerFileCall),
    
    path('investing-calender-json-data/', InvestingCalenderJsonDataAPI),
    path('investing-reuters-json-data/', InvestingReutersJsonDataAPI),
    path('marketing-most-active-json-data/', MarketingMostActiveJsonDataAPI),
    path('marketing-gainer-json-data/', MarketingGainerJsonDataAPI),
    path('marketing-loser-json-data/', MarketingLoserJsonDataAPI),
    path('google-news-json-data/', GoogleNewsJsonDataAPI),
    path('google-finance-json-data/', GoogleFinanceJsonDataAPI),
    path('yahoo-finance-hist-data-api1/', YahooFinanceHistDataAPI1),
    path('json-yahoo-hist-api1/', JsonYahooHistAPI1),
    
    
    path('create-node-data/', JsonNodeDataAPI),
    
    path('create-table-data-json-api/', CreateTableDataJsonAPI , name='create-table-data-json-api'),
    
    path('get-table-dynamic-field/<int:table_id>/', GETTABLEDYNAMICFIELDAPI),
    path('get-table-dynamic-field/<int:table_id>/<str:user_hashkey>/', GETTABLEDYNAMICFIELDAPIHashkey),
    path('get-table-dynamic-field/<int:table_id>/<str:user_id>/', GETTABLEDYNAMICFIELDUSERAPI),
    path('get-table-dynamic-field/<int:table_id>/<str:user_id>/<str:user_hashkey>/', GETTABLEDYNAMICFIELDUSERAPIHashkey),
    path('get-table-dynamic-field-flow/<int:table_id>/<str:flow_name>/', GETTABLEDYNAMICFIELDFLOWAPI),
    
    
    path('rule-validate-frontend/', RuleValidateFrontendAPI),
    path('value-validate-frontend/', ValueValidateFrontendAPI),
    
    path('file-transfer/', FileTransferAPI),
    path('process-name/', ProcessNameAPI),
    path('file-transfer-yahoo-finance-hist/', FileTransferYahooFinanceHistAPI),
    path('file-transfer-yahoo-finance/', FileTransferYahooFinanceAPI),
    path('file-transfer-json/', FileTransferJsonAPI),
    path('file-transfer-investing-json/', FileTransferInvestingJsonAPI),
    path('file-transfer-investing-csv/', FileTransferInvestingCsvAPI),
    
    path('pipe-line-api/', PipeLineApi),
    path('pipe-line-api/<str:user_hashkey>/', PipeLineApiHashKey),
    path('pipe-line-api2/', PipeLineApi2),
    path('pipe-line-api2/<str:user_hashkey>/', PipeLineApiHashKey2),
    path('custom-api-code/', Custom_API_Code),
    path('custom-api-code/<str:user_hashkey>/', Custom_API_CodeHashkey),
    path('custom-code/', Custom_Code),
    path('custom-code-async-test/', Custom_Code_Async_Test),
    path('custom-code/<str:user_hashkey>/', Custom_CodeHashkey),
    path('custom-code-validate/', Custom_Code_Validate),
    path('custom-code-validate/<str:user_hashkey>/', Custom_Code_ValidateHashkey),
    
    path('table-filter-data/', TableFilterDataApi),
    path('table-sort-data/', TableSortDataApi),
    
    
    path('api-formula-calculation/', FormulaCalculationAPIView),
    
    path('json-filter-data-api/', JsonFilterDataAPI),
    path('line-chart-data-api/', LineChartDataAPI),
    path('flow-chart-data/<str:flow_name>/', GETFLOWCHARTDATAAPI),
    path('flow-chart-data/', POSTFLOWCHARTDATAAPI),
    path('flow-chart-data-edge/', POSTFLOWCHARTDATAEDGEAPI),
    path('flow-chart-data-get-api/', POSTFLOWCHARTDATAGETAPI),
    path('flow-chart-data-final-api/', POSTFLOWCHARTFINALAPI),
    
    path('flow-chart-data_api-view/<str:flow_name>/', FlowChartDataAPIVIEW.as_view()),
    
    path('dynamic-get-api/<str:api_name>/<str:user>/', GETUIAPI),
    path('dynamic-post-api/<str:api_name>/<str:user>/', POSTUIAPI),
    path('dynamic-custom2-api/<str:api_name>/<str:user>/', CUSTOM2UIAPI),
    
    path('all-flow-chart-name/', AllFlowChartNameAPI),


    path('yahoo-hist-filename/', YahooHistFileNameAPIVIEW.as_view()),
    path('yahoo-info-filename/', YahooInfoFileNameAPIVIEW.as_view()),
    path('search-like-api/<str:search_key>/', SearchLikeAPI),
    
    path('watch-list-name/', WathListNameAPI),
    path('watch-list-item-name/', WathListItemNameAPI),
    
     path('current-price-historical/', CurrentPriceHistoricalDataAPI),
     
     path('get-dynamic-table-json-field/<int:table_id>/', GETDynamicTableJsonFieldAPI),
    #  path('search-news-data-api/', SearchNewsDataAPI),
    
    path('chat-test/', lobby),
    
    path('change-log/', ChangeLogAPI),
    path('change-log-delete/', ChangeLogDeleteAPI),
    path('change-log-file-transfer/', ChangeLogFileTransferAPI),
    path('pipe-line-delete/<str:api_name>/<str:user>/', PipeLineDeleteAPI),

    path('code-json-write/', CodeJsonWriteAPI),
    path('pipeline-api-create-code-write/', PipeLineAPICreateCodeWriteAPI),
    path('multi-pipeline-api/', MultiPipeLineAPI),
    
    path('get-custom-abc/', CustomABCAPI),
    
    path('job-data/<str:job_name>/', JobDataAPI),
    path('job-delete-api/', JobDeleteAPI),
    
    path('dynamic-get-api1/<str:api_name>/<str:user>/', GETUIDynamicAPI),
    path('d-api/', GETDAPI),
    path('d-json-api/', GETDJSONAPI),
    path('get-file-data-api/', GETFileDataAPI),
    
    path('get-all-table-column/', GETALLTABLECOLUMN),
    
    path('server-process-api/', ServerProcessApi),
    path('server-process-code-api/', ServerProcessCodeApi),
    path('server-process-get-update-delete/', ServerProcessJsonGETUpdateDelete),
    path('server-process-true-data/', ServerProcessTrueData),
    path('validate-api/<str:objType>/<str:ConfKey>/', ValidateApi),
    path('server-on-off-check/', ServerOnOffcheckApi),

    path('one-pointer-calculation/', OnePointerCalculationAPI),
    path('two-pointer-calculation/', TwoPointerCalculationAPI),
    path('two-pointer-summary-calculation/', TwoPointerCalculationSummaryAPI),
    path('two-pointer-minp-calculation/', TwoPointerMinPCalculationAPI),
    path('three-pointer-calculation/', ThreePointerCalculationAPI),
    path('three-pointer-minp-calculation/', ThreePointerMinpCalculationAPI),
    path('three-pointer-d3-calculation/', ThreePointerD3CalculationAPI),
    path('three-pointer-left-right-calculation/<str:apikey>/', ThreePointerLeftRightCalculationAPI),
    path('three-pointer-left-right-day-basis-calculation/', ThreePointerLeftRightDayBasisCalculationAPI),
    path('three-pointer-d3-minp-calculation/', ThreePointerD3MinpCalculationAPI),
    path('four-pointer-left-right-calculation/', FourPointerLeftRightCalculationAPI),
    path('main-pointer-calculation/', MainPointerCalculationAPI),
    path('pointer-summary-data-update-api/', PointerCalculationSummaryDataUpdateAPI),
    path('fetch-new-point-data/', FetchNewPointData),
    path('get-cosine-similarity-api/', GETCosineSimilarityAPI),
    path('send-notification-message-api/', SendNotificationMessageAPI),
    path('get-message-api/<str:email>/', GetMessageAPI),
    path('update-message-api/<str:message_id>/', UpdateMessageAPI),
    path('send-outbound-message-api/', SendOutboundMessageAPI),
    path('send-inbound-message-api/', SendInboundMessageAPI),
    path('balance-simulation-api/', BalanceSimulationAPI),
    path('get-balance-simulation-api/', GETBalanceSimulationAPI),
    path('get-balance-simulation-by-name-api/<str:name>/<str:user_email>/', GETBalanceSimulationByNameAPI),
    path('all-starting-point-api/', ALLStartingPointAPI),
    path('form-builder-data-save-api/', FormBuilderDataSaveAPI),
    path('get-dynamic-table-data-info-api/<int:table_id>/', GETDYNAMICTABLEDATAINFOPI),
    path('get-dynamic-table-data-info-api2/<int:table_id>/', GETDYNAMICTABLEDATAINFOPI2),
    path('update-dynamic-table-data-info-api/', UPDATEDYNAMICTABLEDATAINFOPI),
    path('get-dynamic-json-table-data-info-api/<int:table_id>/<int:user_id>/', GETDYNAMICJSONTABLEDATAINFOPI),
    path('database-connection-mysql/', DatabaseConnectionMySqlAPI),
    # path('page-delete-api/', PageDeleteAPI),
    path('page-wise-data-show-api/<str:page_name>/', PageWiseDataShowAPI),
    path('page-data-clear-api/<str:table_id>/<str:table_col_id>/', PageDataClearAPI),
    path('page-delete-api/<str:table_id>/<str:table_col_id>/<str:page_name>/', PageDeleteAPI),
    path('table-info-dtl-create-api/', TableInfoDtlCreate),
    path('table-col-info-create-api/', TableColInfoCreate),
    path('json-table-data-fetch-api/<str:userId>/', JsonTableDataFetch),
    path('reference-json-table-data-fetch-api/<str:userId>/', ReferenceJsonTableDataFetch),
    path('table-data-fetch-api/<str:userId>/', TableDataFetch),
    path('flowchart-data-fetch-api/<str:userId>/', FlowChartDataFetch),
    path('all-table-data-fetch-api/<str:userId>/', AllTableDataFetch),
    path('get-table-data-rel-id-info-api/', GetTableDataRelIdInfoByUser),
    path('table-data-column-update-api/', TableDataColumnUpdate),
    path('email-send-lalchan/', EmailSendLalchan),

    # path('dynamic-table-get-api/<int:table_id>/<str:user_id>/', DynamicTableGet), #DK
    path('dynamic-table-get-api/', DynamicTableGetAPI), #DK
    path('dynamic-table-create-api/', DynamicTableCreateAPI), #DK
    path('coupon-check-api/', CouponCheckAPI), #DK
    # path('order-confirm-mail-send-api/', OrderConfirmMailSendAPI), #DK
    # path('dynamic-table-delete-api/<int:table_id>/<str:user_id>/<str:table_ref_id>/', DynamicTableDeleteByRefId), #DK

    path('user-role-base-register/', UserRoleBaseRegisterAPI),
    path('user-login/', UserLoginAPI),
    path('user-otp-login/', UserOTPCheckAPI),

]
