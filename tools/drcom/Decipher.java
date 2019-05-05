// 145014129	Nk(Ga!a
// xxy145014129	Mk*Gd#a

// javac filename
// java classname
public class Decipher {

	private static final int MIN_ASC = 32;
	private static final int MAX_ASC = 126;
	private static final int NUM_ASC = 95;
	private static final long MYPRIMENUMBER = 100537L;
	private static final long MYPRIMENUMBER2 = 100609L;
	private static final String KEYWORD = "TblRefreshCurMonthServiceUse";


	public static void main(String[] args)
	{
		System.out.println("============");
		// String from_text = "Nk(Ga!a";
		System.out.println(args[0]);
		String from_text = args[0];
		String a = Decipher(from_text);
		System.out.println(a);
		System.out.println("============");
	}

  public static String Decipher(String from_text)
  {
    char[] word = from_text.toCharArray();
    StringBuilder to_text = new StringBuilder();
    // long key = NumericPassword("TblRefreshCurMonthServiceUse");
    long key = 30137;
    int str_len = from_text.length() - 1;
    for (int i = 0; i < str_len; i++) {
      word[i] = from_text.charAt(i);
      int ch = word[i];
      if ((ch >= 32) && (ch <= 126)) {
        i++;
        ch -= 32;
        double offset = 96.0D * ( key * i % 100537L / 100537.0D);
        ch = (ch - (int)offset) % 95;
        if (ch < 0)
          ch += 95;
        ch += 32;
        i--;
        to_text.append((char)ch);
      }
    }
    return to_text.toString();
  }
/*
  private static long NumericPassword(String password)
  {
    long shift1 = 0L;
    long shift2 = 0L;
    long value = 0L;
    int str_len = password.length();
    for (int i = 0; i < str_len; i++) {
      long ch = password.charAt(i);
      value ^= ch * MyIndex(shift1);
      value ^= ch * MyIndex(shift2);
      shift1 = (shift1 + 7L) % 19L;
      shift2 = (shift2 + 13L) % 23L;
    }
    value = (value ^ 0x18901) % 100537L;
    return value;
  }

  private static long MyIndex(long shadow)
  {
    long j = 1L;
    for (long i = 1L; i <= shadow; i += 1L)
      j *= 2L;
    return j;
  }
*/
}