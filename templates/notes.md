<li>
    <label class="form-label margin-bottom-xxs" for="old-password">Old password</label>
    <div class="password js-password"><input class="yx-n_x form-control yx-me js-password__input" type="password" name="old-password" id="old-password"> <button class="yx-n_k flex yx-ft js-password__btn js-tab-focus"><span class="yx-n__" aria-label="Show password" title="Show password"><i class="text-sm">Show</i></span> <span class="yx-n__" aria-label="Hide password" title="Hide password"><i class="text-sm">Hide</i></span></button></div>
</li>



<li>
<ul class="grid items-center gap-xs">
    <li class="yx-c yx-uo"><label class="form-label" for="autocomplete-input-id">Author</label></li>
    <li class="col">
    <div class="autocomplete yx-ya yx-rtm js-select-auto js-autocomplete" data-autocomplete-dropdown-visible-class="autocomplete--results-visible">
        {% if author %}
        <select class="js-select-auto__select">
        <option>Select author</option>
        <option value="{{author.member.name}}">{{author.member.name}}</option>
        </select>
        {% endif %}
        <div class="yx-rtg" style="--input-btn-icon-size: 12px; --input-btn-icon-margin-right: var(--space-xs);">
        <input class="form-control text-sm yx-padding-nq yx-padding-np js-autocomplete__input js-select-auto__input" type="text" name="author" id="autocomplete-input-id" placeholder="Select author" autocomplete="off">
        <div class="yx-rty">
            <svg class="icon" viewBox="0 0 12 12">
            <title>Open selection</title>
            <polyline points="1 4 6 9 11 4" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></polyline>
            </svg>
            <button class="reset yx-rtb js-select-auto__input-btn js-tab-focus">
            <svg class="icon" viewBox="0 0 16 16">
                <title>Reset selection</title>
                <path d="M8,0a8,8,0,1,0,8,8A8,8,0,0,0,8,0Zm3.707,10.293a1,1,0,1,1-1.414,1.414L8,9.414,5.707,11.707a1,1,0,0,1-1.414-1.414L6.586,8,4.293,5.707A1,1,0,0,1,5.707,4.293L8,6.586l2.293-2.293a1,1,0,1,1,1.414,1.414L9.414,8Z"></path>
            </svg>
            </button>
        </div>
        </div>
        <div class="yx-nqm yx-rtx js-autocomplete__results">
        <ul id="autocomplete1" class="yx-nqg js-autocomplete__list">
            <li class="yx-rtj yx-padding-re yx-padding-nv color-contrast-medium is-hidden js-autocomplete__result" data-autocomplete-template="optgroup" role="presentation"><span class="yx-pt text-sm" data-autocomplete-label></span></li>
            <li class="yx-rtk text-sm yx-padding-re yx-padding-nv is-hidden js-autocomplete__result" data-autocomplete-template="option">
            <span class="is-hidden" data-autocomplete-value></span>
            <div class="yx-pt" data-autocomplete-label></div>
            </li>
            <li class="yx-rtq yx-padding-re yx-padding-nv yx-pt is-hidden js-autocomplete__result" data-autocomplete-template="no-results" role="presentation"></li>
        </ul>
        </div>
        <p class="sr-only" aria-live="polite" aria-atomic="true"><span class="js-autocomplete__aria-results">0</span> results found.</p>
    </div>
    </li>
</ul>
</li>