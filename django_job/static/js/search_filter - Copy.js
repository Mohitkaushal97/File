function init()  {
	presearch_cleanup();
	load_dropdowns();
	init_filter();
}

var locations, isFirstLoad = true;

function load_dropdowns() {
	clear();
	let cookieValues = get_cookies();	
	
	init_locations();

	// Titles
	var cookie_title_ids = cookieValues["title_ids"] ? cookieValues["title_ids"].split("|") : [];
	var cookie_intern_season = cookieValues["intern_season"] ? cookieValues["intern_season"].split("|") : [];
	$.ajax({
		type: "POST",
		url: "web_title_id_and_names",
		success: function(data){
			idAndNames = JSON.parse(data);
			var optTitles = '', isChecked;
			for (var i = 0; i < idAndNames.length; i++) {
				isChecked = cookie_title_ids.indexOf(idAndNames[i][0] + "") !== -1;
				if(idAndNames[i][0] == 1) {
					optTitles+= `<label>
						<input class="unchip" type="checkbox" name="title_option" value="${idAndNames[i][0]}" ${isChecked ? 'checked' : ''} />
						<span>${idAndNames[i][1]}</span>`;

					//add sub list
					optTitles+= `<div class="sub-list" ${isChecked ? 'style="display: block"' : ''}>
						<label>
							<input class="unchip" type="checkbox" name="intern_season" value="1" onchange="javascript:search();" ${cookie_intern_season.indexOf("1") !== -1 ? 'checked' : ''} />
							<span>Spring</span>
						</label>
						<label>
							<input class="unchip" type="checkbox" name="intern_season" value="2" onchange="javascript:search();" ${cookie_intern_season.indexOf("2") !== -1 ? 'checked' : ''}/>
							<span>Summer</span>
						</label>
						<label>
							<input class="unchip" type="checkbox" name="intern_season" value="3" onchange="javascript:search();" ${cookie_intern_season.indexOf("3") !== -1 ? 'checked' : ''}/>
							<span>Fall</span>
						</label>
						<label>
							<input class="unchip" type="checkbox" name="intern_season" value="0" onchange="javascript:search();" ${cookie_intern_season.indexOf("0") !== -1 ? 'checked' : ''}/>
							<span>Uncategorized</span>
						</label>
					</div></label>`;
				} else {
					optTitles+= `<label>
						<input class="unchip" type="checkbox" name="title_option" value="${idAndNames[i][0]}" ${isChecked ? 'checked' : ''} />
						<span>${idAndNames[i][1]}</span>
					</label>`;
				}
			}
			$('#position_titles').html(`<div style="height: 122px;overflow-x: hidden;">${optTitles}</div>`);

			if($("#position_titles [name='title_option']:checked").length > 0) {
				$("#position_titles [name='title_option']:checked").each(function() {
					var $this = $(this);
					$(".search-top .selected-titles").append('<label>' + $this.next("span").text() +' <span data-id="' + $this.val() + '" class="remove"></span></label>');
				});
				$("#clearTitles").fadeIn();
			}
		}
	});
};

function init_locations() {
	let cookieValues = get_cookies();

	if(isFirstLoad && cookieValues["country_id"]) {
		$("#country").val(cookieValues["country_id"]);
		$(".country-dropdown input.select-dropdown").val($("#country option[value='" + cookieValues["country_id"] + "']").text());
		$(".country-dropdown ul.select-dropdown > li").removeClass("selected");
		$(".country-dropdown ul.select-dropdown > li:eq(" + $("#country option[value='" + cookieValues["country_id"] + "']").index() + ")").addClass("selected");
	}

	$("#location .location-list").remove();

	var param = {};
	param['country_id'] = +$("#country").val();

	// Load locations
	var cookie_location_ids = cookieValues["location_ids"] ? cookieValues["location_ids"].split("|") : [];
	$.ajax({
		type: "POST",
		url: "web_location_id_and_names",
		data: param,
		success: function(data){
			idAndNames = JSON.parse(data);
			var optLocations = '';
			for (var i = 0; i < idAndNames.length; i++) {
				optLocations+= `<label data-text="${idAndNames[i][1].toLowerCase()}">
					<input class="unchip" type="checkbox" name="location_option" value="${idAndNames[i][0]}" ${cookie_location_ids.indexOf(idAndNames[i][0] + "") !== -1 ? 'checked' : ''}/>
					<span>${idAndNames[i][1]}</span>
				</label>`;
			}
			$('#location').append(`<div class="location-list">${optLocations}</div>`);

			if($("#location [name='location_option']:checked").length > 0) {
				$("#location [name='location_option']:checked").each(function() {
					var $this = $(this);
					$(".search-top .selected-locations").append('<label>' + $this.next("span").text() +' <span data-id="' + $this.val() + '" class="remove"></span></label>');
				});
				$("#clearLocations").fadeIn();
			}

			search(1, true);
			locations = idAndNames;
		}
	});
}

function init_keywords(keywordsStore) {
	if(!keywordsStore) {
		let cookieValues = get_cookies();
		keywordsStore = [];
		if(cookieValues["keywords"]) {
			var keywords = cookieValues["keywords"].split("|");
			for(var i = 0; i<keywords.length;i++) {
				keywordsStore.push({tag: keywords[i]});
			}
		}
	}
	$('.search-chips-keywords').chips({
		placeholder: 'C++, python, ...',
		secondaryPlaceholder: ' ‏‏‎ ',
		data: keywordsStore,
		autocompleteOptions: {
			limit: Infinity,
			minLength: 1
		},
		onChipAdd: function() {
			var data = $('.search-chips-keywords').chips('getData');
			if(/[,|]+/.test(data[data.length - 1].tag)) {
				var tempData = data[data.length - 1].tag.split(/[,|]+/);
				data.splice(-1, 1);
				for(var i = 0; i < tempData.length; i++) {
					if(!tempData[i]) {
						return;
					}
					data.push({tag : tempData[i]});
				}
				init_keywords(data);
			}
			search();
		},
		onChipDelete: function() {
			search();
		}
	});
}

function search(page_no_requested = 1, hasCleanedUpAlready) {
	if (!hasCleanedUpAlready) {
		presearch_cleanup();
	}

	$('.search-result-loader').show();
	$('.pagination').hide();

	var cookieValues = get_cookies();

	var dict = {};
	dict['page_no_requested'] = page_no_requested;
	dict['country_id'] = +$("#country").val();
	var is_remote = cookieValues["is_remote"];
	if(isFirstLoad && is_remote && is_remote == 1) {
		$('#is_remote').prop("checked", true);
	}
	if ($('#is_remote').is(":checked"))
	{
		is_remote = 1;
		$('[name="location_option"]').prop('disabled', true);
	} else {
		is_remote = 0;
		$('[name="location_option"]').prop('disabled', false);
	}

	if(isFirstLoad && is_remote == 0 && cookieValues["location_ids"]) {
		dict["location_ids"] = cookieValues["location_ids"];
	} else {
		if ($('[name="location_option"]:checked').val())
		{
			dict["location_ids"] = is_remote === 0 ? $('[name="location_option"]:checked').toArray().map(function(location) { return location.value }).join('|') : '';
		}
	}

	if(isFirstLoad && cookieValues["title_ids"]) {
		dict["title_ids"] = cookieValues["title_ids"];
	} else {
		if ($('[name="title_option"]:checked').val())
		{
			dict["title_ids"] = $('[name="title_option"]:checked').toArray().map(function(location) { return location.value }).join('|');
		}
	}

	if(isFirstLoad && cookieValues["intern_season"]) {
		dict["intern_season"] = cookieValues["intern_season"];
	} else {
		if ($('[name="intern_season"]:checked').val())
		{
			dict["intern_season"] = $('[name="intern_season"]:checked').toArray().map(function(location) { return location.value }).join('|');
		}
	}
	dict["keywords"] = isFirstLoad && cookieValues["keywords"] ? cookieValues["keywords"] : $('#keywords').chips('getData').map(function(chip) { return chip.tag}).join('|');
	dict["is_remote"] = is_remote;
	if(isFirstLoad && cookieValues["fresh_graduate"]) {
		$('#fresh_graduate').prop("checked", true);
	}
	dict["fresh_graduate"] = $('#fresh_graduate').is(":checked") ? 1 : 0;
	// dict["total_funding_amount"] = $('[name="funding_option"]:checked').val();
	// dict["engineering_count"] = $('[name="strength_option"]:checked').val();
	if(isFirstLoad && cookieValues["is_fang"]) {
		$('#is_fang').prop("checked", true);
	}
	dict["is_fang"] = $('#is_fang').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["is_unicorn"]) {
		$('#is_unicorn').prop("checked", true);
	}
	dict["is_unicorn"] = $('#is_unicorn').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["is_incubator_company"]) {
		$('#is_incubator_company').prop("checked", true);
	}
	dict["is_incubator_company"] = $('#is_incubator_company').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["is_corporate"]) {
		$('#is_corporate').prop("checked", true);
	}
	dict["is_corporate"] = $('#is_corporate').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["no_cs_needed"]) {
		$('#no_cs_needed').prop("checked", true);
	}
	dict["no_cs_needed"] = $('#no_cs_needed').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["is_non_profit"]) {
		$('#is_non_profit').prop("checked", true);
	}
	dict["is_non_profit"] = $('#is_non_profit').is(':checked') ? 1 : 0;
	if(isFirstLoad && cookieValues["is_contract"]) {
		$('#is_contract').prop("checked", true);
	}
	dict["is_contract"] = $('#is_contract').is(':checked') ? 1 : 0;

	if(!isFirstLoad) {
		reset_coockies();
		$.each(dict, function(key, val) {
			set_cookie(key, val, 30);
		});
	}

	if(isFirstLoad) {
		isFirstLoad = false;
	}

	$.ajax({
		type: "POST",
		url: "search_positions",
		data : dict,
		success: function(data){
			/*ga('send', {
			  hitType: 'event',
			  eventCategory: 'filter_changed',
			  eventAction: 'search_positions'
			});*/
			results = JSON.parse(data);			
			company_to_positions = results && results['positions']
			if (jQuery.isEmptyObject(company_to_positions)) {
				$('#search_results').html(
					`<div class="search-result search-result-none" style="">
						No results were found, please change the filters and try again.
					</div>`
				);
				$('#current_page_no').text(0);
				$('#page_count').text(0);
			} else {
				for (var key in company_to_positions) {
					parts = key.split("_");
					company_id = parts[0];
					company_name = parts[1];
					location_name = parts[2];
					positions = company_to_positions[key]
					for (var i = 0; i < positions.length; i++) {
						var $searchResult = $('#dummy-search-result').clone();
						$searchResult.children('.search-result-heading').text(positions[i]['title_name']).attr('href', positions[i].position_url);
						$searchResult.children('.search-result-company').text(company_name).attr('href', positions[i].company_url);
						$searchResult.children('.search-result-location').text(location_name);
						$searchResult.find('.search-result-people').css('visibility', 'visible').children('span:first').text(positions[i]['nerd_strength']);
						if (!positions[i]['nerd_strength']) {
							$searchResult.find('.search-result-people').css('visibility', 'hidden');
						}
						$searchResult.find('.search-result-funding').show().css('visibility', 'visible').children('span:first').text(positions[i]['funding_raised']);
						if (!positions[i]['funding_raised']) {
							$searchResult.find('.search-result-funding').css('visibility', 'hidden');
							if (positions[i]['stock_url']) {
								$searchResult.find('.search-result-funding').hide();
							}
						}
						if (positions[i]['blog_url']) {
							$searchResult.children('.search-result-blog').attr({
								href: positions[i]['blog_url'],
								target: '_blank',
								rel: 'noopener'
							}).show();
						} else {
							$searchResult.children('.search-result-blog').css("visibility", "hidden");
						}
						if (positions[i]['stock_url']) {
							$searchResult.children('.search-result-stock-chart').attr({
								href: positions[i]['stock_url'],
								target: '_blank',
								rel: 'noopener'
							}).show();
						} else {
							$searchResult.children('.search-result-stock-chart').hide();
						}
						if (positions[i]['company_linkedin_url'] && positions[i]['founders']) {
							$searchResult.children('.search-result-founders').click((function(curl, cname, founders) {
								return function() {
									$('#search-result-founders-popup .links').remove();
									$('#search-result-founders-popup').find('h6:first').after(
										$('<a class="links" href="' + curl + '" target="_blank" rel="noopener">' + cname + '</a>')
									);
									founders.forEach(function(founder) {
										if (founder.founder_linkedin_url) {
											$('#search-result-founders-popup').find('h6:last').after(
												$('<a class="links" href="' + founder.founder_linkedin_url + '">' +
													founder.full_name + ( founder.founder_title ? ' (' + founder.founder_title + ')' : '' ) +
												'</a>')
											);
										} else {
											$('#search-result-founders-popup').find('h6:last').after(
												$('<div class="links">' +
													founder.full_name + ( founder.founder_title ? ' (' + founder.founder_title + ')' : '' ) +
												'</div>')
											);
										}
									});
									$('#search-result-founders-popup').modal('open');
								}
							})(positions[i]['company_linkedin_url'], company_name, positions[i]['founders']));
						} else if (positions[i]['company_linkedin_url']) {
							$searchResult.children('.search-result-founders').attr({
								'href': positions[i]['company_linkedin_url'],
								'target': '_blank',
								'rel': 'noopener'
							});
						} else {
							$searchResult.children('.search-result-founders').hide();
						}
						$searchResult.find('.search-result-posted-on').css('visibility', 'visible').children('span:first').text(positions[i]['posted_on']);
						if (!positions[i]['posted_on']) {
							$searchResult.find('.search-result-posted-on').css('visibility', 'hidden');
						}
						$searchResult.children('.search-result-keywords').empty();
						for (var j = 0; j < positions[i]['stack_terms_in_position'].length; j++) {
							$searchResult.children('.search-result-keywords').append(
								$('<div class="chip">' + positions[i]['stack_terms_in_position'][j] + '</div>')
							);
						}
						$searchResult.children('.search-result-highlights-less').empty();
						$searchResult.children('.search-result-highlights-more').empty();
						if(positions[i]['highlights'] && positions[i]['highlights'].length > 0) {
							var isMore = false;
							for(var j = 0; j < positions[i]['highlights'].length; j++) {
								if(j > 1 || positions[i]['highlights'][j].length > 75) {
									isMore = true;
								}
								if(j <= 1) {
									$searchResult.children('.search-result-highlights-less').append("<li>" + (positions[i]['highlights'][j].substr(0, 75) + (positions[i]['highlights'][j].length > 75 ? "..." : "")) + "</li>");
								}
								$searchResult.children('.search-result-highlights-more').append(`<li>${positions[i]['highlights'][j]}</li>`);
							}
							if(isMore) {
								$(".search-result-highlights-less > li:last", $searchResult).append(`<span class="view-more"> More</span>`);
								$(".search-result-highlights-more > li:last", $searchResult).append(`<span class="view-less"> Less</span>`);
								$searchResult.children('.search-result-highlights-less').show();
								$searchResult.children('.search-result-highlights-more').hide();
							} else {
								$searchResult.children('.search-result-highlights-more').show();
								$searchResult.children('.search-result-highlights-less').hide();
							}
						}
						$('#search_results').append($searchResult.show());
					}
				}
				pagination = results['pagination'];
				$('.current_page_no').text(pagination['current_page_no']);
				$('.page_count').text(pagination['page_count']);
				if(pagination.hasOwnProperty('prev_page_no')) {
					$('.previous_link').attr('onclick', '$(\'html, body\').scrollTop(0);search(' + pagination['prev_page_no'] + ')');
				}
				if(pagination.hasOwnProperty('next_page_no')) {
					$('.next_link').attr('onclick', '$(\'html, body\').scrollTop(0);search(' + pagination['next_page_no'] + ')');
				}
			}
			$('.search-result-loader').hide();
			$('.pagination').show();
			$('.search-result-loader').parent().css("min-height", "");
		}
	});
};

function load_company_info(company_id) {
	var opt = {
		autoOpen: false,
		modal: true,
		width: 600,
		height:250,
		title: 'Company Details',
		position: 'absolute',
		left:475,
		top:100
	};
	var data = {};
	data['company_id'] = company_id;
	$.ajax({
		type: "POST",
		url: "company_details",
		data : data,
		success: function(data){
			company = JSON.parse(data);
			$('#company_url').text(company['url']);
			$('#company_dt_founded').text(company['dt_founded']);
			$('#company_linkedin_url').text(company['linkedin_url']);

			$("#company_dialog").dialog(opt).dialog("open");
		}
	});
}

function clear() {
	$('#search_filter [type="checkbox"]').prop('checked', false);
	$(".selected-locations,.selected-titles").empty();
	$("#clearLocations, #clearTitles").fadeOut();
	$("#position_titles .sub-list").slideUp();
	$('#location_filter').val("");
	$(".location-list > label").removeClass("hidden");
	$(".empty-location-list").hide();
	$(".location-list").show();
	$('#search_results').empty();
	init_keywords();
};

function presearch_cleanup() {
	if($(window).scrollTop() > 0 && screen.height < $(document).height()) {
		$('.search-result-loader').parent().css("min-height", (screen.height + 400) + "px");
	}
	$('.pagination').hide();
	$('#search_results').empty();
	$('.search-result-loader').show();
}

function init_filter() {
	var searchTimeOut, locationStr;
	$('#location_filter').keyup(function(e) {
		if(searchTimeOut) {
			clearTimeout(searchTimeOut);
			searchTimeOut = null;
		}

		searchTimeOut = setTimeout(function() {
			locationStr = $('#location_filter').val().trim();
			$(".location-list > label").removeClass("hidden");
			$(".empty-location-list").hide();
			$(".location-list").show();
			if(locationStr.length < 3) {
				return;
			}

			locationStr = locationStr.toLowerCase();

			$(".location-list > label:not([data-text^='" + locationStr + "'])").addClass("hidden");

			if($(".location-list > label:visible").length == 0) {
				$(".empty-location-list").text("No results found for \"" + locationStr + "\"").show();
				$(".location-list").hide();
			}
		}, 200);
	});

	$("#location").on("change", "[name='location_option']", function() {
		var $this = $(this);
		if($this.is(":checked")) {
			$(".search-top .selected-locations").append('<label>' + $this.next("span").text() +' <span data-id="' + $this.val() + '" class="remove"></span></label>');
		} else {
			$(".search-top .selected-locations [data-id='" + $this.val() + "']").parent().remove();
		}

		if ($('[name="location_option"]:checked').val()) {
			$("#clearLocations").fadeIn();
		} else {
			$("#clearLocations").fadeOut();
		}
		search();
	});

	$("#clearLocations").on("click", function() {
		$("#location [name='location_option']:checked").prop("checked", false);
		$(".search-top .selected-locations > label").remove();
		$("#clearLocations").fadeOut();
		$('#location_filter').val("");
		$(".location-list > label").removeClass("hidden");
		$(".empty-location-list").hide();
		$(".location-list").show();
		search();
	});

	$(".search-top .selected-locations").on("click", ".remove", function() {
		$("#location [name='location_option'][value='" + $(this).attr("data-id") + "']").prop("checked", false).trigger("change");
	});

	//title filter code
	$("#position_titles").on("change", "[name='title_option']", title_change);

	$("#clearTitles").on("click", function() {
		$("#position_titles [name='title_option']:checked").prop("checked", false);
		$(".search-top .selected-titles > label").remove();
		$("#clearTitles").fadeOut();
		search();
	});

	$(".search-top .selected-titles").on("click", ".remove", function() {
		$("#position_titles [name='title_option'][value='" + $(this).attr("data-id") + "']").prop("checked", false).trigger("change");
	});

	//highlights view more and less click
	$('#search_results').on("click", ".search-result-highlights-less .view-more", function() {
		$(this).closest(".search-result-highlights-less").hide();
		$(this).closest(".search-result-highlights-less").siblings('.search-result-highlights-more').show();
	});
	$('#search_results').on("click", ".search-result-highlights-more .view-less", function() {
		$(this).closest(".search-result-highlights-more").hide();
		$(this).closest(".search-result-highlights-more").siblings('.search-result-highlights-less').show();
	});

	//country change
	$("#country").on("change", function() {
		reset_coockies();
		$('.pagination').hide();
		clear();
		$('.search-result-loader').show();
		init_locations();
	});
}

function title_change() {
	var $this = $(this);

	if($this.is(":checked")) {
		$(".search-top .selected-titles").append('<label>' + $this.next("span").text() +' <span data-id="' + $this.val() + '" class="remove"></span></label>');
	} else {
		$(".search-top .selected-titles [data-id='" + $this.val() + "']").parent().remove();
	}

	if ($('#position_titles [name="title_option"]:checked').val()) {
		$("#clearTitles").fadeIn();
	} else {
		$("#clearTitles").fadeOut();
	}

	if($this.parent().find(".sub-list").length == 0) {
		search();
		return;
	}

	if($this.is(":checked")) {
		$this.parent().find(".sub-list").slideDown();
	} else {
		$this.parent().find(".sub-list").slideUp();
		if($this.parent().find(".sub-list").find("[name='intern_season']:checked").length > 0) {
			$this.parent().find(".sub-list").find("[name='intern_season']:checked").each(function() {
				$(this).prop("checked", false);
			});
		}
	}
	search();
}

function set_cookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function get_cookies() {
    var ca = document.cookie.split(';');
	var cookies = {};
    for (var i=0; i<ca.length; i++){
		var pair = ca[i].split("=");
		cookies[(pair[0]+'').trim()] = unescape(pair.slice(1).join('='));
    }
	return cookies;
}
function reset_coockies() {
	var cookies = document.cookie.split(";");
	var custom_cooky_arr = ["page_no_requested","country_id","location_ids","title_ids","intern_season","keywords","is_remote","fresh_graduate","is_fang","is_unicorn","is_incubator_company","is_corporate","no_cs_needed","is_non_profit","is_contract"];

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
		if(name && custom_cooky_arr.indexOf(name.trim()) != -1) {
			document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
		}
    }
}