

#include <iostream>
#include <codecvt>
#include "../pprint.h"
using namespace std;

// http://en.cppreference.com/w/cpp/locale/codecvt_utf8


Pretty pretty;

std::u16string convert_utf8_to_utf16(std::string const& utf8)
{
    // the UTF-8 / UTF-16 standard conversion facet
    std::wstring_convert<std::codecvt_utf8_utf16<char16_t>, char16_t> utf16conv;
    std::u16string utf16 = utf16conv.from_bytes(utf8);
    pretty.select(KRED);
    std::cout <<utf8 <<" has " <<utf16.size() <<" code points:\n";

    pretty.select(KNRM);
    for (char16_t c : utf16)
    {
        std::cout << std::hex << std::showbase << c << ' ';
    }
    cout <<std::oct <<endl;
    return utf16;
}

std::string convert_utf16_to_utf8(std::u16string const& utf16)
{
    std::wstring_convert<std::codecvt_utf8_utf16<char16_t>, char16_t> utf16conv;
    std::string utf8 = utf16conv.to_bytes(utf16);
    return utf8;
}

int main()
{	
    std::u16string a = convert_utf8_to_utf16(u8"Hello 世界!");
    std::u16string b = convert_utf8_to_utf16(u8"はい");

    pretty.select(KGRN);
    cout <<convert_utf16_to_utf8(a) <<endl;
    cout <<convert_utf16_to_utf8(b) <<endl;
    
    

    return 0;
}
