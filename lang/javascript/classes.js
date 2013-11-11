////////////////////////////////////////////////////////////////////////////////
// Author: Healer
// Email: healer_kx@163.com
// 
var classesBeginTime = new Date().getTime();
var hj = hj || {};
var HJ = hj;

var $strings = {};
var $fragments = $fragments || {};
var $groupName = $config['group-name'];

// Mainly for ThinkPHP.
HJ.ACTIONS_PATH             = "/";  // "/index.php/", .htaccess hide the index.php.

HJ.COMMON_WIDGETS_PATH      = "/Tpl/Widgets/";
HJ.COMMON_VIEWS_PATH        = "/Tpl/Views/";

HJ.WIDGETS_PATH             = "/Tpl/" + $groupName + "/Widgets/";
HJ.VIEWS_PATH               = "/Tpl/" + $groupName + "/Views/";


var $log = console.log;
var $warning = $log;


/*******************************************************************************
 * usage:   $class("namespace.Derived-Class-Name", BaseClass | [BaseClass, Mixin1, ...], {
 *              constructor: function() {
 *              },
 *          });
 * 
 *
 */
function $class(d, b, p)
{
    if ( typeof(d) === "string" )
    {
        var superClassName = null;
        if (b)
        {
            if (b instanceof Array)
            {
                superClassName = b[0]._className
            }
            else
            {
                superClassName = b._className;
            }
        }
        var dn = d;

        
        var s = dn.split(/\./);
        
        var w = window;
        var sl = s.length;
        for(var i = 0; i < sl - 1; ++i)
        {
            w = w[s[i]] = w[s[i]] || {};
        }
        
        // An abandoned way
        // d = w[ s[sl - 1] ] = new Function(code);
        d = w[ s[sl - 1] ] = function(){
            var f = function(this_, arguments_, className)
            {
                var clz = $getClassByName(className);
                var superClassName = clz._superClassName;
                if (superClassName)
                {
                    f(this_, arguments_, superClassName);
                }
                if (clz.prototype.__constructor)
                {
                    clz.prototype.__constructor.apply(this_, arguments_);   
                }
            };

            return function(){
                this._className = dn;
                f(this, arguments, dn);
            };
        }(dn);

        // This method would be lost.
    	//d = w[ s[sl - 1] ] = new Function(code);
        d._className = dn;
        d._superClassName = superClassName;

    } else if ( typeof(d) === 'function' ) {
        // d MUST be class Base;
    }

    if (b)
    {
        if (b instanceof Array)
        {
            $.each(b, function(index){
            	$.each(b[index].prototype, function(i, v){
                    if (index > 0)
                    {
                        // TODO:
                        d.prototype[i] = v;
                    }
                    else
              		{
                        d.prototype[i] = v;
                    }
         		});
       		});
        }
        else
        {
            $.each(b.prototype, function(i, v){
          		d.prototype[i] = v;
          	});
        }
    }

    $.each(p, function(i, v){
		d.prototype[i] = v;
  	});

}

function $getClassByName(n)
{
    var s = n.split(/\./);
    var w = window;
    var sl = s.length;
    for(var i = 0; i < sl - 1; ++i)
    {
        w = w[s[i]] = w[s[i]] || {};
    }
    c = w[s[sl -1 ]];
    return c;
}

function $empty(s)
{
	return s == undefined || s == null || s.length == 0;
}

function $random(n)
{
    n = n || 4;
    var rdm = "";
    for(var i = 0; i < n; i++)
        rdm += Math.floor( Math.random() * 10 );
    return rdm;
}

function $stringLoad(fileName, pathName)
{
    if ( $empty(fileName) )
	{
		return "";
	}

    if ( $fragments ) 
    {
        // console.debug('HTML compiled file loaded.');
        var string = $fragments[fileName.toLowerCase()];
        if ( ! $empty(string) )
            return string;
    }

	try
	{
        var string = null;
        var url = pathName + fileName;
        $.ajax({
        	url: url,
         	async: false,
            contentType:"application/x-www-form-urlencoded; charset=utf-8",
         	dataType: 'text',
         	cache: true,
         	type: 'GET',
         	success: function (data, textStatus, jqXHR)
         	{
         		string = data;
            }
        });
        return string;
	}
	catch (e)
	{
		alert("ajax string load failed: " + e.description);
	}
	return "";
}



function $templateString(str, vars)
{
    if ( ! $templateString.templateVarRegex )
    {
        $templateString.templateVarRegex = /\{%\$[a-z0-9-]+%\}/gi;
    }
    var re = $templateString.templateVarRegex;
    var items = str.match(re);
    for (var index in items)
    {
        var item = items[index];
        var key = item.substr(3, item.length - 5);
        str = str.replace(item, vars[key]);
    }
    return str;
}

function $include(fileName, div)
{
    var fgm = $stringLoad(fileName, HJ.VIEWS_PATH);
    
    $(fgm).appendTo(div);
}

function $require(fileName, common)
{
    var widgetPath = common ? HJ.COMMON_WIDGETS_PATH : HJ.WIDGETS_PATH;
    var jsContent = $stringLoad(fileName, widgetPath);
    
    var head = document.getElementsByTagName('HEAD').item(0);
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.text = jsContent;
    head.appendChild( script );

}

function $serviceInvoke(service, data, async, retType, handler)
{
    var retValue = null;
    var httpMethod = data ? "POST" : "GET";
    retType = retType || "text";
    handler = handler || function(retData, textStatus, jqXHR) { retValue = retData; };
    try
    {
        var url = HJ.ACTIONS_PATH + service;
        $.ajax({
            url: url,
            async: async,
            data: data,
            dataType: retType,
            cache: false,
            type: httpMethod,
            success: handler
        });
        return retValue;
    }
    catch (e)
    {
        alert("Service invoke failed: " + e.description);
    }
}


function $bind(receiver, func)
{
    return function(){
        if ( typeof(func) === 'string' )
            return receiver[func].apply(receiver, arguments);
        else
            return func.apply(receiver, arguments);
    };
}

function $g11n(key, lang)
{
    lang = lang || 'zh-cn';
    return $strings[lang][key];
}

///////////////////////////////////////////////////////////////
// For JavaScript has a class named 'Object', 
// so use 'Base' instead of the Inherit-Root.
function Base(){
    Base._className = "Base";
    Base._superClassName = null;
}

$class(Base, null, {

    _className: null,

    __constructor: function()
    {
        //console.debug('Base ctor');
    },

    __super: function(func, args)
    {
        var r = func.apply(this, args);
        return r;
    },


    className: function()
    {
        return this._className;
    },

	toString: function()
	{
		return Base._className;
	}
});
// Init Classes system.,
Base();

$class('EventMixin', null, {
    
    bindEvent: function(domNode, event, handler)
    {
        if (typeof(handler) === "string")
        {
            handler = $bind(this, handler);
        }
        domNode.bind(event, handler);
    },

    bindTextChangedEvent: function(domNode, handler)
    {
        var event = $.browser.msie ? "propertychange" : "input";
        this.bindEvent(domNode, event, handler);
    } 
});

/*
$class('DataStore', Base, {
    __constructor: function()
    {

    }
});
*/



///////////////////////////////////////////////////////////////
$class("kx.Widget", Base, {

    _widgetId: null,

    _domNode: null,

    __constructor: function(widgetId)
    {
        this.__isWeblet = false;
        if (widgetId)
        {
            this._widgetId = widgetId;
        }
        else
        {
            var cn = this._className.toLowerCase();
            this._widgetId = cn + "-" + $random();
        }
    },

    attach: function(domNode)
    {
        this._domNode = domNode;
        this.onAttach && this.onAttach(domNode);
    }


});

///////////////////////////////////////////////////////////////
$class("kx.Weblet", kx.Widget, {

	_templateString: null,

	_templateFile: null,

    _templateVars: null,

    _templateCached: false,

    _common: false,
	
	__constructor: function(widgetId, templateFile)
	{
        this.__isWeblet = true;
        if (templateFile)
        {
            this._templateFile = templateFile;
            this._templateString = null;
        }
	},

	// return domNode, derived class append it to the parent.
	create: function(parent, async)
	{
		if (!this._templateString)
		{
            var widgetPath = this._common ? HJ.COMMON_WIDGETS_PATH : HJ.WIDGETS_PATH;
            if (!async)
            {
                this._templateString = hj.stringLoad(this._templateFile, widgetPath);
            }
            else
            {
                // TODO: Async create a Weblet;
            }
		}

        if (this._templateVars)
        {
            this._templateString = hj.templateString(this._templateString, this._templateVars);
        }

		this._domNode = $(this._templateString);
        this.onCreated && this.onCreated(this._domNode);
		return this._domNode;
	},

    setCommon: function()
    {
        this._common = true;
    },

    widgetId: function()
    {
        return this._widgetId;
    },

    findNodes: function(sel)
    {
        return this._domNode.find(sel);
    },

    hide: function(hidden)
    {
        var dv = hidden;
        if ( hidden == false || hidden == 'false' )
        {
            dv = '';
        }
        else if ( !hidden || hidden == true || hidden == 'true' )
        {
            dv = 'none';
        }
        this._domNode.css('display', dv)
    },

    destroy: function()
    {
        this._domNode.remove();
    },

	toString: function()
	{
		return "Widget";
	}


});

// Type Alias;

Widget = kx.Weblet;



// Static Methods
Widget.load = function( widgetName, common )
{
    var widgetClass = $getClassByName(widgetName);
    if ( !widgetClass )
    {
        var path = widgetName.replace(/\./g, "/") + ".js";
        $require(path, common);
        widgetClass = $getClassByName(widgetName);
    }
    return widgetClass
}

Widget.addWidget = function( widget )
{
    if ( !Widget.widgetsArray )
    {
        Widget.widgetsArray = [];
    }
    var widgetId = widget.widgetId();
    if ( !Widget.widgetById(widgetId) )
    {
        Widget.widgetsArray[widgetId] = widget;
        return true;
    }
    $warning('Duplicated Widget ID');
    return false;
};

Widget.widgetById = function(widgetId)
{
    if ( !Widget.widgetsArray )
    {
        return null;
    }
    return Widget.widgetsArray[widgetId];
};

Widget.isWidget = function(widget)
{
    if ( typeof(widget) == 'object' )
    {
        if ( !widget._widgetId )
        {
            return false;
        }

        return true;
    }
    return false;
};

// Mixin.
$class('ActionMixin', null, {

    _actionBase: 'Home/',

    // For ThinkPHP.
    invokeAction: function(action, data, handler)
    {
        if (!this.invokeAction.re)
        {
            this.invokeAction.re = /(.*)Action\.(.*)/;
        }
        var re = this.invokeAction.re;
        var m = action.match(re);

        var service = this._actionBase + m[1] + '/' + m[2];
        return this.ajax(service, data, handler);
    },

    ajax: function(service, data, handler)
    {
        return $serviceInvoke(service, data, true, 'text', $bind(this, function(){
            if ( typeof(handler) == 'string' )
            {
                this[handler].apply(this, arguments);
            }
            else if ( typeof(handler) == 'function' )
            {
                handler.apply(this, arguments);
            }
        }));
    }


});

function $compare(a, b, d)
{
    if (a == b)
    {
        return 0;
    }
    else if ( a < b )
    {
        return d;
    }
    else
    {
        return -d;
    }
}


function onBodyResize()
{
    $('body').trigger('onsize');
}

function $main(args)
{
    $process(args, $('body'));
}


function $process(args, node)
{
    var includes = node.attr('includes');

    if ('none' !== includes)
    {
        node.find('div[include]').each(function(){
            var div = $(this);
            var file = div.attr('include');

            if ( !$empty(file) )
            {
                $include(file, div);
            }
        });
    }

    // Widget contains kx.Widget and kx.Weblet;
    // <div widget-class='' widget-id='' widget-path='' async='false|true'/>
    node.find('div[widget-class]').each(function(){
        var div = $(this);
        var widgetClassName = div.attr('widget-class');
        var common = div.attr('common');
        if ( !$empty(widgetClassName) )
        {
            
            var widgetClass = $getClassByName(widgetClassName);
            var widgetId = div.attr('widget-id');
            // console.debug(widgetClassName);
            var widget = new widgetClass(widgetId);
            if (common)
            {
                widget.setCommon();
            }
            if (widget.__isWeblet)
            {
                widget.create(div);
            }
            else
            {
                widget.attach(div);   
            }
            Widget.addWidget( widget );
        }
    });

    if (classesBeginTime)
    {
        // This time can be calculated as initialized time.
        var classesEndTime = new Date().getTime();
        console.debug( "Main function takes " + (classesEndTime - classesBeginTime) + " ms" );
    }

}



////////////////////////////////////////////////////////////////////////////////
hj.stringLoad       = $stringLoad;
hj.templateString   = $templateString;
hj.bind             = $bind;
hj.empty            = $empty;
////////////////////////////////////////////////////////////////////////////////

String.prototype.endsWith = function(p) {
    return this.indexOf(p) + p.length == this.length;
};



